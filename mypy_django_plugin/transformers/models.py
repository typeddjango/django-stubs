from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Tuple, cast

import dataclasses
from mypy.nodes import (
    ARG_POS, ARG_STAR, ARG_STAR2, MDEF, Argument, CallExpr, ClassDef, Expression, IndexExpr, MemberExpr, MypyFile,
    NameExpr, StrExpr, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import ClassDefContext
from mypy.plugins.common import add_method
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import AnyType, Instance, NoneTyp, TypeOfAny

from mypy_django_plugin.lib import metadata, fullnames, helpers


@dataclasses.dataclass
class ModelClassInitializer(metaclass=ABCMeta):
    api: SemanticAnalyzerPass2
    model_classdef: ClassDef
    app_models_mapping: Optional[Dict[str, str]] = None

    @classmethod
    def from_ctx(cls, ctx: ClassDefContext, app_models_mapping: Optional[Dict[str, str]]):
        return cls(api=cast(SemanticAnalyzerPass2, ctx.api),
                   model_classdef=ctx.cls,
                   app_models_mapping=app_models_mapping)

    def get_meta_attribute(self, name: str) -> Optional[Expression]:
        meta_node = helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None

        return helpers.get_assignment_stmt_by_name(meta_node, name)

    def is_abstract_model(self) -> bool:
        is_abstract_expr = self.get_meta_attribute('abstract')
        if is_abstract_expr is None:
            return False
        return self.api.parse_bool(is_abstract_expr)

    def add_new_node_to_model_class(self, name: str, typ: Instance) -> None:
        # type=: type of the variable itself
        var = Var(name=name, type=typ)
        # var.info: type of the object variable is bound to
        var.info = self.model_classdef.info
        var._fullname = self.model_classdef.info.fullname() + '.' + name
        var.is_inferred = True
        var.is_initialized_in_class = True
        self.model_classdef.info.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True)

    def model_has_name_defined(self, name: str) -> bool:
        return name in self.model_classdef.info.names

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()


def iter_over_one_to_n_related_fields(klass: ClassDef) -> Iterator[Tuple[NameExpr, CallExpr]]:
    for field_name, field_init in helpers.iter_over_field_inits_in_class(klass):
        field_info = field_init.callee.node
        assert isinstance(field_info, TypeInfo)

        if helpers.has_any_of_bases(field_init.callee.node, {fullnames.FOREIGN_KEY_FULLNAME,
                                                             fullnames.ONETOONE_FIELD_FULLNAME}):
            yield field_name, field_init


class AddReferencesToRelatedModels(ModelClassInitializer):
    """
    For every
        attr1 = models.ForeignKey(to=MyModel)
    sets `attr1_id` attribute to the current model.
    """

    def run(self) -> None:
        for field_name, field_init_expr in helpers.iter_over_field_inits_in_class(self.model_classdef):
            ref_id_name = field_name + '_id'
            field_info = field_init_expr.callee.node
            assert isinstance(field_info, TypeInfo)

            if not self.model_has_name_defined(ref_id_name):
                if helpers.has_any_of_bases(field_info, {fullnames.FOREIGN_KEY_FULLNAME,
                                                         fullnames.ONETOONE_FIELD_FULLNAME}):
                    self.add_new_node_to_model_class(name=ref_id_name,
                                                     typ=self.api.builtin_type('builtins.int'))

        #     field_init_expr.callee.node
        #
        # for field_name, field_init_expr in helpers.iter_call_assignments_in_class(self.model_classdef):
        #     ref_id_name = field_name + '_id'
        #     if not self.model_has_name_defined(ref_id_name):
        #         field_class_info = field_init_expr.callee.node
        #         if not field_class_info:
        #
        #         if not field_init_expr.callee.node:
        #
        #         if isinstance(field_init_expr.callee.node, TypeInfo) \
        #                 and helpers.has_any_of_bases(field_init_expr.callee.node,
        #                                              {fullnames.FOREIGN_KEY_FULLNAME,
        #                                               fullnames.ONETOONE_FIELD_FULLNAME}):
        #             self.add_new_node_to_model_class(name=ref_id_name,
        #                                              typ=self.api.builtin_type('builtins.int'))


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
        meta_node = helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddDefaultObjectsManager(ModelClassInitializer):
    def _add_new_manager(self, name: str, manager_type: Optional[Instance]) -> None:
        if manager_type is None:
            return None
        self.add_new_node_to_model_class(name, manager_type)

    def _add_private_default_manager(self, manager_type: Optional[Instance]) -> None:
        if manager_type is None:
            return None
        self.add_new_node_to_model_class('_default_manager', manager_type)

    def _get_existing_managers(self) -> List[Tuple[str, TypeInfo]]:
        managers = []
        for base in self.model_classdef.info.mro:
            for manager_name, call_expr in helpers.iter_call_assignments_in_class(base.defn):
                callee_expr = call_expr.callee
                if isinstance(callee_expr, IndexExpr):
                    callee_expr = callee_expr.analyzed.expr

                if isinstance(callee_expr, (MemberExpr, NameExpr)) \
                        and isinstance(callee_expr.node, TypeInfo) \
                        and callee_expr.node.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
                    managers.append((manager_name, callee_expr.node))
        return managers

    def run(self) -> None:
        existing_managers = self._get_existing_managers()
        if existing_managers:
            first_manager_type = None
            for manager_name, manager_type_info in existing_managers:
                manager_type = Instance(manager_type_info, args=[Instance(self.model_classdef.info, [])])
                self._add_new_manager(name=manager_name, manager_type=manager_type)
                if first_manager_type is None:
                    first_manager_type = manager_type
        else:
            if self.is_abstract_model():
                # abstract models do not need 'objects' queryset
                return None

            first_manager_type = self.api.named_type_or_none(fullnames.MANAGER_CLASS_FULLNAME,
                                                             args=[Instance(self.model_classdef.info, [])])
            self._add_new_manager('objects', manager_type=first_manager_type)

        if self.is_abstract_model():
            return None
        default_manager_name_expr = self.get_meta_attribute('default_manager_name')
        if isinstance(default_manager_name_expr, StrExpr):
            self._add_private_default_manager(self.model_classdef.info.get(default_manager_name_expr.value).type)
        else:
            self._add_private_default_manager(first_manager_type)


class AddDefaultPrimaryKey(ModelClassInitializer):
    """
    Sets default integer `id` attribute, if:
        * model is not abstract (abstract = False)
        * there's no field with primary_key=True
    """

    def run(self) -> None:
        if self.is_abstract_model():
            # abstract models cannot be instantiated, and do not need `id` attribute
            return None

        for _, field_init_expr in helpers.iter_over_field_inits_in_class(self.model_classdef):
            if ('primary_key' in field_init_expr.arg_names
                    and self.api.parse_bool(field_init_expr.args[field_init_expr.arg_names.index('primary_key')])):
                break
        else:
            self.add_new_node_to_model_class('id', self.api.builtin_type('builtins.int'))


def _get_to_expr(field_init_expr) -> Expression:
    if 'to' in field_init_expr.arg_names:
        return field_init_expr.args[field_init_expr.arg_names.index('to')]
    else:
        return field_init_expr.args[0]


class AddRelatedManagers(ModelClassInitializer):
    def _add_related_manager_variable(self, manager_name: str, related_field_type_data: Dict[str, Any]) -> None:
        # add dummy related manager for use later
        self.add_new_node_to_model_class(manager_name, self.api.builtin_type('builtins.object'))

        # save name in metadata for use in get_attribute_hook later
        related_managers_metadata = metadata.get_related_managers_metadata(self.model_classdef.info)
        related_managers_metadata[manager_name] = related_field_type_data

    def run(self) -> None:
        for module_name, module_file in self.api.modules.items():
            for model_classdef in helpers.iter_over_toplevel_classes(module_file):
                for field_name, field_init in helpers.iter_over_field_inits_in_class(model_classdef):
                    field_info = field_init.callee.node
                    assert isinstance(field_info, TypeInfo)

                    if helpers.has_any_of_bases(field_info, fullnames.RELATED_FIELDS_CLASSES):
                        # try:
                        to_arg_expr = _get_to_expr(field_init)
                        if isinstance(to_arg_expr, NameExpr):
                            referenced_model_fullname = module_file.names[to_arg_expr.name].fullname
                        else:
                            assert isinstance(to_arg_expr, StrExpr)
                            value = to_arg_expr.value
                            if value == 'self':
                                # reference to the same model class
                                referenced_model_fullname = model_classdef.fullname
                            elif '.' not in value:
                                # reference to class in the current module
                                referenced_model_fullname = module_name + '.' + value
                            else:
                                referenced_model_fullname = self.app_models_mapping[value]

                            # referenced_model_fullname = extract_referenced_model_fullname(field_init,
                            #                                                               module_file=module_file,
                            #                                                               all_modules=self.api.modules)
                            # if not referenced_model_fullname:
                            #     raise helpers.IncompleteDefnException('Cannot parse referenced model fullname')

                        # except helpers.SelfReference:
                        #     referenced_model_fullname = model_classdef.fullname
                        #
                        # except helpers.SameFileModel as exc:
                        #     referenced_model_fullname = module_name + '.' + exc.model_cls_name

                        if self.model_classdef.fullname == referenced_model_fullname:
                            if 'related_name' in field_init.arg_names:
                                related_name_expr = field_init.args[field_init.arg_names.index('related_name')]
                                if not isinstance(related_name_expr, StrExpr):
                                    # not string 'related_name=' not yet supported
                                    continue
                                related_name = related_name_expr.value
                                if related_name == '+':
                                    # No backwards relation is desired
                                    continue
                            else:
                                related_name = model_classdef.name.lower() + '_set'

                            # Default related_query_name to related_name
                            if 'related_query_name' in field_init.arg_names:
                                related_query_name_expr = field_init.args[field_init.arg_names.index('related_query_name')]
                                if isinstance(related_query_name_expr, StrExpr):
                                    related_query_name = related_query_name_expr.value
                                else:
                                    # not string 'related_query_name=' is not yet supported
                                    related_query_name = None
                                # TODO: Handle defaulting to model name if related_name is not set
                            else:
                                related_query_name = related_name

                            # if helpers.has_any_of_bases(field_info, {fullnames.FOREIGN_KEY_FULLNAME,
                            #                                          fullnames.MANYTOMANY_FIELD_FULLNAME}):
                            #     # as long as Model is not a Generic, one level depth is fine
                            #     field_type_data = {
                            #         'manager': fullnames.RELATED_MANAGER_CLASS_FULLNAME,
                            #         'of': [model_classdef.info.fullname()]
                            #     }
                            # else:
                            #     field_type_data = {
                            #         'manager': model_classdef.info.fullname(),
                            #         'of': []
                            #     }
                            self.add_new_node_to_model_class(related_name, self.api.builtin_type('builtins.object'))

                            # self._add_related_manager_variable(related_name, related_field_type_data=field_type_data)

                            if related_query_name is not None:
                                # Only create related_query_name if it is a string literal
                                metadata.get_lookups_metadata(self.model_classdef.info)[related_query_name] = {
                                    'related_query_name_target': related_name
                                }


def get_related_field_type(rvalue: CallExpr, related_model_typ: TypeInfo) -> Dict[str, Any]:
    if rvalue.callee.name in {'ForeignKey', 'ManyToManyField'}:
        return {
            'manager': fullnames.RELATED_MANAGER_CLASS_FULLNAME,
            'of': [related_model_typ.fullname()]
        }
    else:
        return {
            'manager': related_model_typ.fullname(),
            'of': []
        }


def is_related_field(expr: CallExpr, module_file: MypyFile) -> bool:
    """ Checks whether current CallExpr represents any supported RelatedField subclass"""
    if isinstance(expr.callee, MemberExpr) and isinstance(expr.callee.expr, NameExpr):
        module = module_file.names.get(expr.callee.expr.name)
        if module \
                and module.fullname == 'django.db.models' \
                and expr.callee.name in {'ForeignKey',
                                         'OneToOneField',
                                         'ManyToManyField'}:
            return True
    return False


def extract_referenced_model_fullname(field_init_expr: CallExpr,
                                      module_file: MypyFile,
                                      all_modules: Dict[str, MypyFile]) -> Optional[str]:
    """ Returns fullname of a Model referenced in "to=" argument of the CallExpr"""
    if 'to' in field_init_expr.arg_names:
        to_expr = field_init_expr.args[field_init_expr.arg_names.index('to')]
    else:
        to_expr = field_init_expr.args[0]

    if isinstance(to_expr, NameExpr):
        return module_file.names[to_expr.name].fullname

    elif isinstance(to_expr, StrExpr):
        typ_fullname = helpers.get_model_fullname_from_string(to_expr.value, all_modules)
        if typ_fullname is None:
            return None
        return typ_fullname

    return None


def add_dummy_init_method(ctx: ClassDefContext) -> None:
    any = AnyType(TypeOfAny.special_form)

    pos_arg = Argument(variable=Var('args', any),
                       type_annotation=any, initializer=None, kind=ARG_STAR)
    kw_arg = Argument(variable=Var('kwargs', any),
                      type_annotation=any, initializer=None, kind=ARG_STAR2)

    add_method(ctx, '__init__', [pos_arg, kw_arg], NoneTyp())

    # mark as model class
    ctx.cls.info.metadata.setdefault('django', {})['generated_init'] = True


def add_get_set_attr_fallback_to_any(ctx: ClassDefContext):
    any = AnyType(TypeOfAny.special_form)

    name_arg = Argument(variable=Var('name', any),
                        type_annotation=any, initializer=None, kind=ARG_POS)
    add_method(ctx, '__getattr__', [name_arg], any)

    value_arg = Argument(variable=Var('value', any),
                         type_annotation=any, initializer=None, kind=ARG_POS)
    add_method(ctx, '__setattr__', [name_arg, value_arg], any)


def process_model_class(ctx: ClassDefContext,
                        ignore_unknown_attributes: bool,
                        app_models_mapping: Optional[Dict[str, str]]) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultPrimaryKey,
        AddReferencesToRelatedModels,
        AddDefaultObjectsManager,
        AddRelatedManagers,
    ]
    for initializer_cls in initializers:
        initializer_cls.from_ctx(ctx, app_models_mapping).run()

    add_dummy_init_method(ctx)

    if ignore_unknown_attributes:
        add_get_set_attr_fallback_to_any(ctx)
