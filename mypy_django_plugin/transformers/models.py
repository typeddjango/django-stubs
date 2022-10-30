from typing import Any, Dict, List, Optional, Type, Union, cast

from django.db.models import Manager, Model
from django.db.models.fields import DateField, DateTimeField, Field
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel, OneToOneRel
from mypy.checker import TypeChecker
from mypy.nodes import ARG_STAR2, Argument, AssignmentStmt, CallExpr, Context, NameExpr, TypeInfo, Var
from mypy.plugin import AnalyzeTypeContext, AttributeContext, CheckerPluginInterface, ClassDefContext
from mypy.plugins import common
from mypy.semanal import SemanticAnalyzer
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypedDictType, TypeOfAny, get_proper_type
from mypy.typevars import fill_typevars

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.errorcodes import MANAGER_MISSING
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.lib.fullnames import ANNOTATIONS_FULLNAME, ANY_ATTR_ALLOWED_CLASS_FULLNAME, MODEL_CLASS_FULLNAME
from mypy_django_plugin.transformers import fields
from mypy_django_plugin.transformers.fields import get_field_descriptor_types
from mypy_django_plugin.transformers.managers import (
    MANAGER_METHODS_RETURNING_QUERYSET,
    create_manager_info_from_from_queryset_call,
)


class ModelClassInitializer:
    api: SemanticAnalyzer

    def __init__(self, ctx: ClassDefContext, django_context: DjangoContext) -> None:
        self.api = cast(SemanticAnalyzer, ctx.api)
        self.model_classdef = ctx.cls
        self.django_context = django_context
        self.ctx = ctx

    def lookup_typeinfo(self, fullname: str) -> Optional[TypeInfo]:
        return helpers.lookup_fully_qualified_typeinfo(self.api, fullname)

    def lookup_typeinfo_or_incomplete_defn_error(self, fullname: str) -> TypeInfo:
        info = self.lookup_typeinfo(fullname)
        if info is None:
            raise helpers.IncompleteDefnException(f"No {fullname!r} found")
        return info

    def lookup_class_typeinfo_or_incomplete_defn_error(self, klass: type) -> TypeInfo:
        fullname = helpers.get_class_fullname(klass)
        field_info = self.lookup_typeinfo_or_incomplete_defn_error(fullname)
        return field_info

    def create_new_var(self, name: str, typ: MypyType) -> Var:
        # type=: type of the variable itself
        var = Var(name=name, type=typ)
        # var.info: type of the object variable is bound to
        var.info = self.model_classdef.info
        var._fullname = self.model_classdef.info.fullname + "." + name
        var.is_initialized_in_class = True
        var.is_inferred = True
        return var

    def add_new_node_to_model_class(self, name: str, typ: MypyType, no_serialize: bool = False) -> None:
        helpers.add_new_sym_for_info(self.model_classdef.info, name=name, sym_type=typ, no_serialize=no_serialize)

    def add_new_class_for_current_module(self, name: str, bases: List[Instance]) -> TypeInfo:
        current_module = self.api.modules[self.model_classdef.info.module_name]
        new_class_info = helpers.add_new_class_for_module(current_module, name=name, bases=bases)
        return new_class_info

    def run(self) -> None:
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.fullname)
        if model_cls is None:
            return
        self.run_with_model_cls(model_cls)

    def get_generated_manager_mappings(self, base_manager_fullname: str) -> Dict[str, str]:
        base_manager_info = self.lookup_typeinfo(base_manager_fullname)
        if base_manager_info is None or "from_queryset_managers" not in base_manager_info.metadata:
            return {}
        return base_manager_info.metadata["from_queryset_managers"]

    def get_generated_manager_info(self, manager_fullname: str, base_manager_fullname: str) -> Optional[TypeInfo]:
        generated_managers = self.get_generated_manager_mappings(base_manager_fullname)
        real_manager_fullname = generated_managers.get(manager_fullname)
        if real_manager_fullname:
            return self.lookup_typeinfo(real_manager_fullname)
        # Not a generated manager
        return None

    def get_or_create_manager_with_any_fallback(self, related_manager: bool = False) -> TypeInfo:
        """
        Create a Manager subclass with fallback to Any for unknown attributes
        and methods. This is used for unresolved managers, where we don't know
        the actual type of the manager.

        The created class is reused if multiple unknown managers are encountered.
        """

        name = "UnknownManager" if not related_manager else "UnknownRelatedManager"

        # Check if we've already created a fallback manager class for this
        # module, and if so reuse that.
        manager_info = self.lookup_typeinfo(f"{self.model_classdef.info.module_name}.{name}")
        if manager_info and manager_info.metadata.get("django", {}).get("any_fallback_manager"):
            return manager_info

        fallback_queryset = self.get_or_create_queryset_with_any_fallback()
        base_manager_fullname = (
            fullnames.MANAGER_CLASS_FULLNAME if not related_manager else fullnames.RELATED_MANAGER_CLASS
        )
        base_manager_info = self.lookup_typeinfo(base_manager_fullname)
        assert base_manager_info, f"Type info for {base_manager_fullname} missing"

        base_manager = fill_typevars(base_manager_info)
        assert isinstance(base_manager, Instance)
        manager_info = self.add_new_class_for_current_module(name, [base_manager])
        manager_info.fallback_to_any = True

        manager_info.type_vars = base_manager_info.type_vars
        manager_info.defn.type_vars = base_manager_info.defn.type_vars
        manager_info.metaclass_type = manager_info.calculate_metaclass_type()

        # For methods on BaseManager that return a queryset we need to update
        # the return type to be the actual queryset subclass used. This is done
        # by adding the methods as attributes with type Any to the manager
        # class. The actual type of these methods are resolved in
        # resolve_manager_method.
        for method_name in MANAGER_METHODS_RETURNING_QUERYSET:
            helpers.add_new_sym_for_info(
                manager_info, name=method_name, sym_type=AnyType(TypeOfAny.implementation_artifact)
            )

        manager_info.metadata["django"] = {
            "any_fallback_manager": True,
            "from_queryset_manager": fallback_queryset.fullname,
        }

        return manager_info

    def get_or_create_queryset_with_any_fallback(self) -> TypeInfo:
        """
        Create a QuerySet subclass with fallback to Any for unknown attributes
        and methods. This is used for the manager returned by the method above.
        """

        name = "UnknownQuerySet"

        # Check if we've already created a fallback queryset class for this
        # module, and if so reuse that.
        queryset_info = self.lookup_typeinfo(f"{self.model_classdef.info.module_name}.{name}")
        if queryset_info and queryset_info.metadata.get("django", {}).get("any_fallback_queryset"):
            return queryset_info

        base_queryset_info = self.lookup_typeinfo(fullnames.QUERYSET_CLASS_FULLNAME)
        assert base_queryset_info, f"Type info for {fullnames.QUERYSET_CLASS_FULLNAME} missing"

        base_queryset = fill_typevars(base_queryset_info)
        assert isinstance(base_queryset, Instance)
        queryset_info = self.add_new_class_for_current_module(name, [base_queryset])
        queryset_info.metadata["django"] = {
            "any_fallback_queryset": True,
        }
        queryset_info.fallback_to_any = True

        queryset_info.type_vars = base_queryset_info.type_vars.copy()
        queryset_info.defn.type_vars = base_queryset_info.defn.type_vars.copy()
        queryset_info.metaclass_type = queryset_info.calculate_metaclass_type()

        return queryset_info

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        raise NotImplementedError("Implement this in subclasses")


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


class AddDefaultPrimaryKey(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        auto_field = model_cls._meta.auto_field
        if auto_field:
            self.create_autofield(
                auto_field=auto_field,
                dest_name=auto_field.attname,
                existing_field=not self.model_classdef.info.has_readable_member(auto_field.attname),
            )

    def create_autofield(
        self,
        auto_field: "Field[Any, Any]",
        dest_name: str,
        existing_field: bool,
    ) -> None:
        if existing_field:
            auto_field_fullname = helpers.get_class_fullname(auto_field.__class__)
            auto_field_info = self.lookup_typeinfo_or_incomplete_defn_error(auto_field_fullname)

            set_type, get_type = fields.get_field_descriptor_types(
                auto_field_info,
                is_set_nullable=True,
                is_get_nullable=False,
            )

            self.add_new_node_to_model_class(dest_name, Instance(auto_field_info, [set_type, get_type]))


class AddPrimaryKeyAlias(AddDefaultPrimaryKey):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # We also need to override existing `pk` definition from `stubs`:
        auto_field = model_cls._meta.pk
        if auto_field:
            self.create_autofield(
                auto_field=auto_field,
                dest_name="pk",
                existing_field=self.model_classdef.info.has_readable_member(auto_field.name),
            )


class AddRelatedModelsId(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        for field in model_cls._meta.get_fields():
            if isinstance(field, ForeignKey):
                related_model_cls = self.django_context.get_field_related_model_cls(field)
                if related_model_cls is None:
                    error_context: Context = self.ctx.cls
                    field_sym = self.ctx.cls.info.get(field.name)
                    if field_sym is not None and field_sym.node is not None:
                        error_context = field_sym.node
                    self.api.fail(
                        f"Cannot find model {field.related_model!r} referenced in field {field.name!r}",
                        ctx=error_context,
                    )
                    self.add_new_node_to_model_class(field.attname, AnyType(TypeOfAny.explicit))
                    continue

                if related_model_cls._meta.abstract:
                    continue

                rel_target_field = self.django_context.get_related_target_field(related_model_cls, field)
                if not rel_target_field:
                    continue

                try:
                    field_info = self.lookup_class_typeinfo_or_incomplete_defn_error(rel_target_field.__class__)
                except helpers.IncompleteDefnException as exc:
                    if not self.api.final_iteration:
                        raise exc
                    else:
                        continue

                is_nullable = self.django_context.get_field_nullability(field, None)
                set_type, get_type = get_field_descriptor_types(
                    field_info, is_set_nullable=is_nullable, is_get_nullable=is_nullable
                )
                self.add_new_node_to_model_class(field.attname, Instance(field_info, [set_type, get_type]))


class AddManagers(ModelClassInitializer):
    def has_any_parametrized_manager_as_base(self, info: TypeInfo) -> bool:
        for base in helpers.iter_bases(info):
            if self.is_any_parametrized_manager(base):
                return True
        return False

    def is_any_parametrized_manager(self, typ: Instance) -> bool:
        return typ.type.fullname in fullnames.MANAGER_CLASSES and isinstance(typ.args[0], AnyType)

    def lookup_manager(self, fullname: str, manager: "Manager[Any]") -> Optional[TypeInfo]:
        manager_info = self.lookup_typeinfo(fullname)
        if manager_info is None:
            manager_info = self.get_dynamic_manager(fullname, manager)
        return manager_info

    def is_manager_dynamically_generated(self, manager_info: Optional[TypeInfo]) -> bool:
        if manager_info is None:
            return False
        return manager_info.metadata.get("django", {}).get("from_queryset_manager") is not None

    def reparametrize_dynamically_created_manager(self, manager_name: str, manager_info: Optional[TypeInfo]) -> None:
        if not self.is_manager_dynamically_generated(manager_info):
            return

        assert manager_info is not None
        # Reparameterize dynamically created manager with model type
        manager_type = Instance(manager_info, [Instance(self.model_classdef.info, [])])
        self.add_new_node_to_model_class(manager_name, manager_type)

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        manager_info: Optional[TypeInfo]

        incomplete_manager_defs = set()
        for manager_name, manager in model_cls._meta.managers_map.items():
            manager_node = self.model_classdef.info.names.get(manager_name, None)
            manager_fullname = helpers.get_class_fullname(manager.__class__)
            manager_info = self.lookup_manager(manager_fullname, manager)

            if manager_node and manager_node.type is not None:
                # Manager is already typed -> do nothing unless it's a dynamically generated manager
                self.reparametrize_dynamically_created_manager(manager_name, manager_info)
                continue

            if manager_info is None:
                # We couldn't find a manager type, see if we should create one
                manager_info = self.create_manager_from_from_queryset(manager_name)

            if manager_info is None:
                incomplete_manager_defs.add(manager_name)
                continue

            manager_type = Instance(manager_info, [Instance(self.model_classdef.info, [])])
            self.add_new_node_to_model_class(manager_name, manager_type)

        if incomplete_manager_defs:
            if not self.api.final_iteration:
                #  Unless we're on the final round, see if another round could
                #  figure out all manager types
                raise helpers.IncompleteDefnException()

            for manager_name in incomplete_manager_defs:
                # We act graceful and set the type as the bare minimum we know of
                # (Django's default) before finishing. And emit an error, to allow for
                # ignoring a more specialised manager not being resolved while still
                # setting _some_ type
                fallback_manager_info = self.get_or_create_manager_with_any_fallback()
                self.add_new_node_to_model_class(
                    manager_name, Instance(fallback_manager_info, [Instance(self.model_classdef.info, [])])
                )

                # Find expression for e.g. `objects = SomeManager()`
                manager_expr = self.get_manager_expression(manager_name)
                manager_fullname = f"{self.model_classdef.fullname}.{manager_name}"
                self.api.fail(
                    f'Could not resolve manager type for "{manager_fullname}"',
                    manager_expr if manager_expr else self.ctx.cls,
                    code=MANAGER_MISSING,
                )

    def get_manager_expression(self, name: str) -> Optional[AssignmentStmt]:
        # TODO: What happens if the manager is defined multiple times?
        for expr in self.ctx.cls.defs.body:
            if (
                isinstance(expr, AssignmentStmt)
                and isinstance(expr.lvalues[0], NameExpr)
                and expr.lvalues[0].name == name
            ):
                return expr

        return None

    def get_dynamic_manager(self, fullname: str, manager: "Manager[Any]") -> Optional[TypeInfo]:
        """
        Try to get a dynamically defined manager
        """

        # Check if manager is a generated (dynamic class) manager
        base_manager_fullname = helpers.get_class_fullname(manager.__class__.__bases__[0])
        generated_managers = self.get_generated_manager_mappings(base_manager_fullname)

        generated_manager_name: Optional[str] = generated_managers.get(fullname, None)
        if generated_manager_name is None:
            return None

        return self.lookup_typeinfo(generated_manager_name)

    def create_manager_from_from_queryset(self, name: str) -> Optional[TypeInfo]:
        """
        Try to create a manager from a .from_queryset call:

            class MyModel(models.Model):
                objects = MyManager.from_queryset(MyQuerySet)()
        """

        assign_statement = self.get_manager_expression(name)
        if assign_statement is None:
            return None

        expr = assign_statement.rvalue
        if not isinstance(expr, CallExpr) or not isinstance(expr.callee, CallExpr):
            return None

        return create_manager_info_from_from_queryset_call(self.api, expr.callee)


class AddDefaultManagerAttribute(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        if "_default_manager" in self.model_classdef.info.names:
            return None

        default_manager_cls = model_cls._meta.default_manager.__class__
        default_manager_fullname = helpers.get_class_fullname(default_manager_cls)

        try:
            default_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(default_manager_fullname)
        except helpers.IncompleteDefnException as exc:
            # Check if default manager could be a generated manager
            base_manager_fullname = helpers.get_class_fullname(default_manager_cls.__bases__[0])
            generated_manager_info = self.get_generated_manager_info(default_manager_fullname, base_manager_fullname)
            if generated_manager_info is None:
                # Manager doesn't appear to be generated. Unless we're on the final round,
                # see if another round could help figuring out the default manager type
                if not self.api.final_iteration:
                    raise exc
                else:
                    return None
            default_manager_info = generated_manager_info

        default_manager = Instance(default_manager_info, [Instance(self.model_classdef.info, [])])
        self.add_new_node_to_model_class("_default_manager", default_manager)


class AddRelatedManagers(ModelClassInitializer):
    def get_reverse_manager_info(self, model_info: TypeInfo, derived_from: str) -> Optional[TypeInfo]:
        manager_fullname = helpers.get_django_metadata(model_info).get("reverse_managers", {}).get(derived_from)
        if not manager_fullname:
            return None

        symbol = self.api.lookup_fully_qualified_or_none(manager_fullname)
        if symbol is None or not isinstance(symbol.node, TypeInfo):
            return None
        return symbol.node

    def set_reverse_manager_info(self, model_info: TypeInfo, derived_from: str, fullname: str) -> None:
        helpers.get_django_metadata(model_info).setdefault("reverse_managers", {})[derived_from] = fullname

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # add related managers
        for relation in self.django_context.get_model_relations(model_cls):
            attname = relation.get_accessor_name()
            if attname is None or attname in self.model_classdef.info.names:
                # No reverse accessor or already declared. Note that this would also leave any
                # explicitly declared(i.e. non-inferred) reverse accessors alone
                continue

            related_model_cls = self.django_context.get_field_related_model_cls(relation)
            if related_model_cls is None:
                continue

            try:
                related_model_info = self.lookup_class_typeinfo_or_incomplete_defn_error(related_model_cls)
            except helpers.IncompleteDefnException as exc:
                if not self.api.final_iteration:
                    raise exc
                else:
                    continue

            if isinstance(relation, OneToOneRel):
                self.add_new_node_to_model_class(attname, Instance(related_model_info, []))
                continue

            if isinstance(relation, (ManyToOneRel, ManyToManyRel)):
                related_manager_info = None
                try:
                    related_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(
                        fullnames.RELATED_MANAGER_CLASS
                    )  # noqa: E501
                    default_manager = related_model_info.names.get("_default_manager")
                    if not default_manager:
                        raise helpers.IncompleteDefnException()
                except helpers.IncompleteDefnException as exc:
                    if not self.api.final_iteration:
                        raise exc

                    # If a django model has a Manager class that cannot be
                    # resolved statically (if it is generated in a way where we
                    # cannot import it, like `objects = my_manager_factory()`),
                    # we fallback to the default related manager, so you at
                    # least get a base level of working type checking.
                    #
                    # See https://github.com/typeddjango/django-stubs/pull/993
                    # for more information on when this error can occur.
                    fallback_manager = self.get_or_create_manager_with_any_fallback(related_manager=True)
                    self.add_new_node_to_model_class(
                        attname, Instance(fallback_manager, [Instance(related_model_info, [])])
                    )
                    related_model_fullname = related_model_cls.__module__ + "." + related_model_cls.__name__
                    self.ctx.api.fail(
                        (
                            "Couldn't resolve related manager for relation "
                            f"{relation.name!r} (from {related_model_fullname}."
                            f"{relation.field})."
                        ),
                        self.ctx.cls,
                        code=MANAGER_MISSING,
                    )

                    continue

                # Check if the related model has a related manager subclassed from the default manager
                # TODO: Support other reverse managers than `_default_manager`
                default_reverse_manager_info = self.get_reverse_manager_info(
                    model_info=related_model_info, derived_from="_default_manager"
                )
                if default_reverse_manager_info:
                    self.add_new_node_to_model_class(attname, Instance(default_reverse_manager_info, []))
                    continue

                # The reverse manager we're looking for doesn't exist. So we
                # create it. The (default) reverse manager type is built from a
                # RelatedManager and the default manager on the related model
                parametrized_related_manager_type = Instance(related_manager_info, [Instance(related_model_info, [])])
                default_manager_type = default_manager.type
                assert default_manager_type is not None
                assert isinstance(default_manager_type, Instance)
                # When the default manager isn't custom there's no need to create a new type
                # as `RelatedManager` has `models.Manager` as base
                if default_manager_type.type.fullname == fullnames.MANAGER_CLASS_FULLNAME:
                    self.add_new_node_to_model_class(attname, parametrized_related_manager_type)
                    continue

                # The reverse manager is based on the related model's manager, so it makes most sense to add the new
                # related manager in that module
                new_related_manager_info = helpers.add_new_class_for_module(
                    module=self.api.modules[related_model_info.module_name],
                    name=f"{related_model_cls.__name__}_RelatedManager",
                    bases=[parametrized_related_manager_type, default_manager_type],
                )
                new_related_manager_info.metadata["django"] = {"related_manager_to_model": related_model_info.fullname}
                # Stash the new reverse manager type fullname on the related model, so we don't duplicate
                # or have to create it again for other reverse relations
                self.set_reverse_manager_info(
                    related_model_info,
                    derived_from="_default_manager",
                    fullname=new_related_manager_info.fullname,
                )
                self.add_new_node_to_model_class(attname, Instance(new_related_manager_info, []))


class AddExtraFieldMethods(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # get_FOO_display for choices
        for field in self.django_context.get_model_fields(model_cls):
            if field.choices:
                info = self.lookup_typeinfo_or_incomplete_defn_error("builtins.str")
                return_type = Instance(info, [])
                common.add_method(self.ctx, name=f"get_{field.attname}_display", args=[], return_type=return_type)

        # get_next_by, get_previous_by for Date, DateTime
        for field in self.django_context.get_model_fields(model_cls):
            if isinstance(field, (DateField, DateTimeField)) and not field.null:
                return_type = Instance(self.model_classdef.info, [])
                common.add_method(
                    self.ctx,
                    name=f"get_next_by_{field.attname}",
                    args=[
                        Argument(
                            Var("kwargs", AnyType(TypeOfAny.explicit)),
                            AnyType(TypeOfAny.explicit),
                            initializer=None,
                            kind=ARG_STAR2,
                        )
                    ],
                    return_type=return_type,
                )
                common.add_method(
                    self.ctx,
                    name=f"get_previous_by_{field.attname}",
                    args=[
                        Argument(
                            Var("kwargs", AnyType(TypeOfAny.explicit)),
                            AnyType(TypeOfAny.explicit),
                            initializer=None,
                            kind=ARG_STAR2,
                        )
                    ],
                    return_type=return_type,
                )


class AddMetaOptionsAttribute(ModelClassInitializer):
    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        if "_meta" not in self.model_classdef.info.names:
            options_info = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.OPTIONS_CLASS_FULLNAME)
            self.add_new_node_to_model_class("_meta", Instance(options_info, [Instance(self.model_classdef.info, [])]))


def process_model_class(ctx: ClassDefContext, django_context: DjangoContext) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultPrimaryKey,
        AddPrimaryKeyAlias,
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
        except helpers.IncompleteDefnException:
            if not ctx.api.final_iteration:
                ctx.api.defer()


def set_auth_user_model_boolean_fields(ctx: AttributeContext, django_context: DjangoContext) -> MypyType:
    boolinfo = helpers.lookup_class_typeinfo(helpers.get_typechecker_api(ctx), bool)
    assert boolinfo is not None
    return Instance(boolinfo, [])


def handle_annotated_type(ctx: AnalyzeTypeContext, django_context: DjangoContext) -> MypyType:
    args = ctx.type.args
    type_arg = ctx.api.analyze_type(args[0])
    api = cast(SemanticAnalyzer, ctx.api.api)  # type: ignore

    if not isinstance(type_arg, Instance) or not type_arg.type.has_base(MODEL_CLASS_FULLNAME):
        return type_arg

    fields_dict = None
    if len(args) > 1:
        second_arg_type = get_proper_type(ctx.api.analyze_type(args[1]))
        if isinstance(second_arg_type, TypedDictType):
            fields_dict = second_arg_type
        elif isinstance(second_arg_type, Instance) and second_arg_type.type.fullname == ANNOTATIONS_FULLNAME:
            annotations_type_arg = get_proper_type(second_arg_type.args[0])
            if isinstance(annotations_type_arg, TypedDictType):
                fields_dict = annotations_type_arg
            elif not isinstance(annotations_type_arg, AnyType):
                ctx.api.fail("Only TypedDicts are supported as type arguments to Annotations", ctx.context)

    return get_or_create_annotated_type(api, type_arg, fields_dict=fields_dict)


def get_or_create_annotated_type(
    api: Union[SemanticAnalyzer, CheckerPluginInterface], model_type: Instance, fields_dict: Optional[TypedDictType]
) -> Instance:
    """

    Get or create the type for a model for which you getting/setting any attr is allowed.

    The generated type is an subclass of the model and django._AnyAttrAllowed.
    The generated type is placed in the django_stubs_ext module, with the name WithAnnotations[ModelName].
    If the user wanted to annotate their code using this type, then this is the annotation they would use.
    This is a bit of a hack to make a pretty type for error messages and which would make sense for users.
    """
    model_module_name = "django_stubs_ext"

    if helpers.is_annotated_model_fullname(model_type.type.fullname):
        # If it's already a generated class, we want to use the original model as a base
        model_type = model_type.type.bases[0]

    if fields_dict is not None:
        type_name = f"WithAnnotations[{model_type.type.fullname.replace('.', '__')}, {fields_dict}]"
    else:
        type_name = f"WithAnnotations[{model_type.type.fullname.replace('.', '__')}]"

    annotated_typeinfo = helpers.lookup_fully_qualified_typeinfo(
        cast(TypeChecker, api), model_module_name + "." + type_name
    )
    if annotated_typeinfo is None:
        model_module_file = api.modules[model_module_name]  # type: ignore

        if isinstance(api, SemanticAnalyzer):
            annotated_model_type = api.named_type_or_none(ANY_ATTR_ALLOWED_CLASS_FULLNAME, [])
            assert annotated_model_type is not None
        else:
            annotated_model_type = api.named_generic_type(ANY_ATTR_ALLOWED_CLASS_FULLNAME, [])

        annotated_typeinfo = helpers.add_new_class_for_module(
            model_module_file,
            type_name,
            bases=[model_type] if fields_dict is not None else [model_type, annotated_model_type],
            fields=fields_dict.items if fields_dict is not None else None,
            no_serialize=True,
        )
        if fields_dict is not None:
            # To allow structural subtyping, make it a Protocol
            annotated_typeinfo.is_protocol = True
            # Save for later to easily find which field types were annotated
            annotated_typeinfo.metadata["annotated_field_types"] = fields_dict.items
    annotated_type = Instance(annotated_typeinfo, [])
    return annotated_type
