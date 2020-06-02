from typing import List, Optional, Type, cast

from django.db.models.base import Model
from django.db.models.fields import DateField, DateTimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.fields.reverse_related import (
    ManyToManyRel, ManyToOneRel, OneToOneRel,
)
from mypy.nodes import (
    ARG_STAR2, GDEF, MDEF, Argument, Context, FuncDef, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import ClassDefContext
from mypy.plugins import common
from mypy.semanal import SemanticAnalyzer, dummy_context
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers, sem_helpers
from mypy_django_plugin.transformers import fields
from mypy_django_plugin.transformers.fields import get_field_descriptor_types


class ModelClassInitializer:
    api: SemanticAnalyzer

    def __init__(self, ctx: ClassDefContext, django_context: DjangoContext):
        self.api = cast(SemanticAnalyzer, ctx.api)
        self.model_classdef = ctx.cls
        self.django_context = django_context
        self.ctx = ctx

    def lookup_typeinfo(self, fullname: str) -> Optional[TypeInfo]:
        return helpers.lookup_fully_qualified_typeinfo(self.api, fullname)

    def lookup_typeinfo_or_incomplete_defn_error(self, fullname: str) -> TypeInfo:
        info = self.lookup_typeinfo(fullname)
        if info is None:
            raise sem_helpers.IncompleteDefnException(f'No {fullname!r} found')
        return info

    def lookup_class_typeinfo_or_incomplete_defn_error(self, klass: type) -> TypeInfo:
        fullname = helpers.get_class_fullname(klass)
        field_info = self.lookup_typeinfo_or_incomplete_defn_error(fullname)
        return field_info

    def model_class_has_attribute_defined(self, name: str, traverse_mro: bool = True) -> bool:
        if not traverse_mro:
            sym = self.model_classdef.info.names.get(name)
        else:
            sym = self.model_classdef.info.get(name)
        return sym is not None

    def resolve_manager_fullname(self, manager_fullname: str) -> str:
        base_manager_info = self.lookup_typeinfo(fullnames.MANAGER_CLASS_FULLNAME)
        if (base_manager_info is None
                or 'from_queryset_managers' not in base_manager_info.metadata):
            return manager_fullname

        metadata = base_manager_info.metadata['from_queryset_managers']
        return metadata.get(manager_fullname, manager_fullname)

    def add_new_node_to_model_class(self, name: str, typ: MypyType,
                                    force_replace_existing: bool = False) -> None:
        if not force_replace_existing and name in self.model_classdef.info.names:
            raise ValueError(f'Member {name!r} already defined at model {self.model_classdef.info.fullname!r}.')

        var = Var(name, type=typ)
        # TypeInfo of the object variable is bound to
        var.info = self.model_classdef.info
        var._fullname = self.api.qualified_name(name)
        var.is_initialized_in_class = True

        sym = SymbolTableNode(MDEF, var, plugin_generated=True)
        context: Optional[Context] = dummy_context()
        if force_replace_existing:
            context = None
        self.api.add_symbol_table_node(name, sym, context=context)

    def add_new_class_for_current_module(self, name: str, bases: List[Instance],
                                         force_replace_existing: bool = False) -> TypeInfo:
        current_module = self.api.cur_mod_node
        if not force_replace_existing and name in current_module.names:
            raise ValueError(f'Class {name!r} already defined for module {current_module.fullname!r}')

        new_typeinfo = helpers.new_typeinfo(name,
                                            bases=bases,
                                            module_name=current_module.fullname)
        if name in current_module.names:
            del current_module.names[name]
        current_module.names[name] = SymbolTableNode(GDEF, new_typeinfo, plugin_generated=True)
        return new_typeinfo

    def run(self) -> None:
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.fullname)
        if model_cls is None:
            return
        self.run_with_model_cls(model_cls)

    def run_with_model_cls(self, model_cls):
        pass


class InjectAnyAsBaseForNestedMeta(ModelClassInitializer):
    """
    Replaces
        class MyModel(models.Model):
            class Meta:
                pass
    with
        class MyModel(models.Model):
            class Meta(Any):
                pass
    to get around incompatible Meta inner classes for different models.
    """

    def run(self) -> None:
        meta_node = sem_helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddDefaultPrimaryKey(ModelClassInitializer):
    """
    Adds default primary key to models which does not define their own.
    ```
        class User(models.Model):
            name = models.TextField()
    ```
    """

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        auto_field = model_cls._meta.auto_field
        if auto_field is None:
            return

        primary_key_attrname = auto_field.attname
        if self.model_class_has_attribute_defined(primary_key_attrname):
            return

        auto_field_class_fullname = helpers.get_class_fullname(auto_field.__class__)
        auto_field_info = self.lookup_typeinfo_or_incomplete_defn_error(auto_field_class_fullname)

        set_type, get_type = fields.get_field_descriptor_types(auto_field_info, is_nullable=False)
        self.add_new_node_to_model_class(primary_key_attrname, Instance(auto_field_info,
                                                                        [set_type, get_type]))


class AddRelatedModelsId(ModelClassInitializer):
    """
    Adds `FIELDNAME_id` attributes to models.
    ```
        class User(models.Model):
            pass
        class Blog(models.Model):
            user = models.ForeignKey(User)
    ```

     `user_id` will be added to `Blog`.
    """

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        for field in model_cls._meta.get_fields():
            if not isinstance(field, (OneToOneField, ForeignKey)):
                continue
            related_id_attr_name = field.attname
            if self.model_class_has_attribute_defined(related_id_attr_name):
                continue
            # if self.get_model_class_attr(related_id_attr_name) is not None:
            #     continue

            related_model_cls = self.django_context.get_field_related_model_cls(field)
            if related_model_cls is None:
                error_context: Context = self.ctx.cls
                field_sym = self.ctx.cls.info.get(field.name)
                if field_sym is not None and field_sym.node is not None:
                    error_context = field_sym.node
                self.api.fail(f'Cannot find model {field.related_model!r} '
                              f'referenced in field {field.name!r} ',
                              ctx=error_context)
                self.add_new_node_to_model_class(related_id_attr_name,
                                                 AnyType(TypeOfAny.explicit))
                continue

            if related_model_cls._meta.abstract:
                continue

            rel_primary_key_field = self.django_context.get_primary_key_field(related_model_cls)
            try:
                field_info = self.lookup_class_typeinfo_or_incomplete_defn_error(rel_primary_key_field.__class__)
            except sem_helpers.IncompleteDefnException as exc:
                if not self.api.final_iteration:
                    raise exc
                else:
                    continue

            is_nullable = self.django_context.get_field_nullability(field, None)
            set_type, get_type = get_field_descriptor_types(field_info, is_nullable)
            self.add_new_node_to_model_class(related_id_attr_name,
                                             Instance(field_info, [set_type, get_type]))


class AddManagers(ModelClassInitializer):
    def has_any_parametrized_manager_as_base(self, info: TypeInfo) -> bool:
        for base in helpers.iter_bases(info):
            if self.is_any_parametrized_manager(base):
                return True
        return False

    def is_any_parametrized_manager(self, typ: Instance) -> bool:
        return typ.type.fullname in fullnames.MANAGER_CLASSES and isinstance(typ.args[0], AnyType)

    def create_new_model_parametrized_manager(self, name: str, base_manager_info: TypeInfo) -> Instance:
        bases = []
        for original_base in base_manager_info.bases:
            if self.is_any_parametrized_manager(original_base):
                original_base = helpers.reparametrize_instance(original_base,
                                                               [Instance(self.model_classdef.info, [])])
            bases.append(original_base)

        new_manager_info = self.add_new_class_for_current_module(name, bases, force_replace_existing=True)
        # copy fields to a new manager
        new_cls_def_context = ClassDefContext(cls=new_manager_info.defn,
                                              reason=self.ctx.reason,
                                              api=self.api)
        custom_manager_type = Instance(new_manager_info, [Instance(self.model_classdef.info, [])])

        for name, sym in base_manager_info.names.items():
            if name in new_manager_info.names:
                raise ValueError(f'Name {name!r} already exists on newly-created {new_manager_info.fullname!r} class.')

            # replace self type with new class, if copying method
            if isinstance(sym.node, FuncDef):
                sem_helpers.copy_method_or_incomplete_defn_exception(new_cls_def_context,
                                                                     self_type=custom_manager_type,
                                                                     new_method_name=name,
                                                                     method_node=sym.node)
                continue

            new_sym = sym.copy()
            if isinstance(new_sym.node, Var):
                new_var = Var(name, type=sym.type)
                new_var.info = new_manager_info
                new_var._fullname = new_manager_info.fullname + '.' + name
                new_sym.node = new_var

            new_manager_info.names[name] = new_sym

        return custom_manager_type

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        for manager_name, manager in model_cls._meta.managers_map.items():
            if self.model_class_has_attribute_defined(manager_name, traverse_mro=False):
                sym = self.model_classdef.info.names.get(manager_name)
                assert sym is not None

                if (sym.type is not None
                        and isinstance(sym.type, Instance)
                        and sym.type.type.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME)
                        and not self.has_any_parametrized_manager_as_base(sym.type.type)):
                    # already defined and parametrized properly
                    continue

            if getattr(manager, '_built_with_as_manager', False):
                # as_manager is not supported yet
                if not self.model_class_has_attribute_defined(manager_name, traverse_mro=True):
                    self.add_new_node_to_model_class(manager_name, AnyType(TypeOfAny.explicit))
                continue

            manager_fullname = self.resolve_manager_fullname(helpers.get_class_fullname(manager.__class__))
            manager_info = self.lookup_typeinfo_or_incomplete_defn_error(manager_fullname)
            manager_class_name = manager_fullname.rsplit('.', maxsplit=1)[1]

            if manager_name not in self.model_classdef.info.names:
                # manager not yet defined, just add models.Manager[ModelName]
                manager_type = Instance(manager_info, [Instance(self.model_classdef.info, [])])
                self.add_new_node_to_model_class(manager_name, manager_type)
            else:
                # creates new MODELNAME_MANAGERCLASSNAME class that represents manager parametrized with current model
                if not self.has_any_parametrized_manager_as_base(manager_info):
                    continue

                custom_model_manager_name = manager.model.__name__ + '_' + manager_class_name
                custom_manager_type = self.create_new_model_parametrized_manager(custom_model_manager_name,
                                                                                 base_manager_info=manager_info)

                self.add_new_node_to_model_class(manager_name, custom_manager_type,
                                                 force_replace_existing=True)


class AddDefaultManagerAttribute(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        if self.model_class_has_attribute_defined('_default_manager', traverse_mro=False):
            return
        if model_cls._meta.default_manager is None:
            return
        if getattr(model_cls._meta.default_manager, '_built_with_as_manager', False):
            self.add_new_node_to_model_class('_default_manager',
                                             AnyType(TypeOfAny.explicit))
            return

        default_manager_fullname = helpers.get_class_fullname(model_cls._meta.default_manager.__class__)
        resolved_default_manager_fullname = self.resolve_manager_fullname(default_manager_fullname)

        default_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(resolved_default_manager_fullname)
        default_manager = Instance(default_manager_info, [Instance(self.model_classdef.info, [])])
        self.add_new_node_to_model_class('_default_manager', default_manager)


class AddRelatedManagers(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # add related managers
        for relation in self.django_context.get_model_relations(model_cls):
            related_manager_attr_name = relation.get_accessor_name()
            if related_manager_attr_name is None:
                # no reverse accessor
                continue

            if self.model_class_has_attribute_defined(related_manager_attr_name, traverse_mro=False):
                continue

            related_model_cls = self.django_context.get_field_related_model_cls(relation)
            if related_model_cls is None:
                continue

            try:
                related_model_info = self.lookup_class_typeinfo_or_incomplete_defn_error(related_model_cls)
            except sem_helpers.IncompleteDefnException as exc:
                if not self.api.final_iteration:
                    raise exc
                else:
                    continue

            if isinstance(relation, OneToOneRel):
                self.add_new_node_to_model_class(related_manager_attr_name, Instance(related_model_info, []))
                continue

            if isinstance(relation, (ManyToOneRel, ManyToManyRel)):
                try:
                    related_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(
                        fullnames.RELATED_MANAGER_CLASS)  # noqa: E501
                    if 'objects' not in related_model_info.names:
                        raise sem_helpers.IncompleteDefnException()
                except sem_helpers.IncompleteDefnException as exc:
                    if not self.api.final_iteration:
                        raise exc
                    else:
                        continue

                # create new RelatedManager subclass
                parametrized_related_manager_type = Instance(related_manager_info,
                                                             [Instance(related_model_info, [])])
                default_manager_type = related_model_info.names['objects'].type
                if (default_manager_type is None
                        or not isinstance(default_manager_type, Instance)
                        or default_manager_type.type.fullname == fullnames.MANAGER_CLASS_FULLNAME):
                    self.add_new_node_to_model_class(related_manager_attr_name, parametrized_related_manager_type)
                    continue

                name = related_model_cls.__name__ + '_' + 'RelatedManager'
                bases = [parametrized_related_manager_type, default_manager_type]
                new_related_manager_info = self.add_new_class_for_current_module(name, bases,
                                                                                 force_replace_existing=True)
                self.add_new_node_to_model_class(related_manager_attr_name,
                                                 Instance(new_related_manager_info, []))


class AddExtraFieldMethods(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # get_FOO_display for choices
        for field in self.django_context.get_model_fields(model_cls):
            if field.choices:
                info = self.lookup_typeinfo_or_incomplete_defn_error('builtins.str')
                return_type = Instance(info, [])
                common.add_method(self.ctx,
                                  name='get_{}_display'.format(field.attname),
                                  args=[],
                                  return_type=return_type)

        # get_next_by, get_previous_by for Date, DateTime
        for field in self.django_context.get_model_fields(model_cls):
            if isinstance(field, (DateField, DateTimeField)) and not field.null:
                return_type = Instance(self.model_classdef.info, [])
                common.add_method(self.ctx,
                                  name='get_next_by_{}'.format(field.attname),
                                  args=[Argument(Var('kwargs', AnyType(TypeOfAny.explicit)),
                                                 AnyType(TypeOfAny.explicit),
                                                 initializer=None,
                                                 kind=ARG_STAR2)],
                                  return_type=return_type)
                common.add_method(self.ctx,
                                  name='get_previous_by_{}'.format(field.attname),
                                  args=[Argument(Var('kwargs', AnyType(TypeOfAny.explicit)),
                                                 AnyType(TypeOfAny.explicit),
                                                 initializer=None,
                                                 kind=ARG_STAR2)],
                                  return_type=return_type)


class AddMetaOptionsAttribute(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        if '_meta' not in self.model_classdef.info.names:
            options_info = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.OPTIONS_CLASS_FULLNAME)
            self.add_new_node_to_model_class('_meta',
                                             Instance(options_info, [
                                                 Instance(self.model_classdef.info, [])
                                             ]))


def process_model_class(ctx: ClassDefContext,
                        django_context: DjangoContext) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultPrimaryKey,
        AddRelatedModelsId,
        AddManagers,
        AddDefaultManagerAttribute,
        AddRelatedManagers,
        AddExtraFieldMethods,
        AddMetaOptionsAttribute,
    ]
    for initializer_cls in initializers:
        try:
            initializer_cls(ctx, django_context).run()
        except sem_helpers.IncompleteDefnException as exc:
            if not ctx.api.final_iteration:
                ctx.api.defer()
                continue
            raise exc
