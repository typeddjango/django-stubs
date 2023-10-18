from functools import cached_property
from typing import Any, Dict, List, Optional, Type, Union, cast

from django.db.models import Manager, Model
from django.db.models.fields import DateField, DateTimeField, Field
from django.db.models.fields.reverse_related import ForeignObjectRel, OneToOneRel
from mypy.checker import TypeChecker
from mypy.nodes import (
    ARG_STAR2,
    MDEF,
    Argument,
    AssignmentStmt,
    CallExpr,
    Context,
    Expression,
    NameExpr,
    RefExpr,
    StrExpr,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import AnalyzeTypeContext, AttributeContext, CheckerPluginInterface, ClassDefContext
from mypy.plugins import common
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import TypeAnalyser
from mypy.types import AnyType, Instance, ProperType, TypedDictType, TypeOfAny, TypeType, get_proper_type
from mypy.types import Type as MypyType
from mypy.typevars import fill_typevars

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.errorcodes import MANAGER_MISSING
from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.lib.fullnames import ANNOTATIONS_FULLNAME, ANY_ATTR_ALLOWED_CLASS_FULLNAME, MODEL_CLASS_FULLNAME
from mypy_django_plugin.transformers.fields import get_field_descriptor_types
from mypy_django_plugin.transformers.managers import (
    MANAGER_METHODS_RETURNING_QUERYSET,
    create_manager_info_from_from_queryset_call,
)
from mypy_django_plugin.transformers.manytomany import M2MArguments, M2MThrough, M2MTo, get_model_from_expression


class ModelClassInitializer:
    api: SemanticAnalyzer

    def __init__(self, ctx: ClassDefContext, django_context: DjangoContext) -> None:
        self.api = cast(SemanticAnalyzer, ctx.api)
        self.model_classdef = ctx.cls
        self.django_context = django_context
        self.ctx = ctx

    @property
    def is_model_abstract(self) -> bool:
        return helpers.is_abstract_model(self.model_classdef.info)

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

    def add_new_node_to_model_class(
        self, name: str, typ: MypyType, *, no_serialize: bool = False, is_classvar: bool = False
    ) -> None:
        # TODO: Rename to signal that it is a `Var` that is added..
        helpers.add_new_sym_for_info(
            self.model_classdef.info, name=name, sym_type=typ, no_serialize=no_serialize, is_classvar=is_classvar
        )

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

    def get_or_create_manager_with_any_fallback(self, related_manager: bool = False) -> Optional[TypeInfo]:
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
        if fallback_queryset is None:
            return None
        base_manager_fullname = (
            fullnames.MANAGER_CLASS_FULLNAME if not related_manager else fullnames.RELATED_MANAGER_CLASS
        )
        base_manager_info = self.lookup_typeinfo(base_manager_fullname)
        if base_manager_info is None:
            return None

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

    def get_or_create_queryset_with_any_fallback(self) -> Optional[TypeInfo]:
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
        if base_queryset_info is None:
            return None

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
        raise NotImplementedError(f"Implement this in subclass {self.__class__.__name__}")


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

            set_type, get_type = get_field_descriptor_types(
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
        for field in self.django_context.get_model_foreign_keys(model_cls):
            try:
                related_model_cls = self.django_context.get_field_related_model_cls(field)
            except UnregisteredModelError:
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
        self.add_new_node_to_model_class(manager_name, manager_type, is_classvar=True)

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
            self.add_new_node_to_model_class(manager_name, manager_type, is_classvar=True)

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
                if fallback_manager_info is not None:
                    self.add_new_node_to_model_class(
                        manager_name,
                        Instance(fallback_manager_info, [Instance(self.model_classdef.info, [])]),
                        is_classvar=True,
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
        self.add_new_node_to_model_class("_default_manager", default_manager, is_classvar=True)


class AddReverseLookups(ModelClassInitializer):
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
        reverse_one_to_one_descriptor = self.lookup_typeinfo_or_incomplete_defn_error(
            fullnames.REVERSE_ONE_TO_ONE_DESCRIPTOR
        )
        # add related managers
        for relation in self.django_context.get_model_relations(model_cls):
            attname = relation.get_accessor_name()
            if attname is None or attname in self.model_classdef.info.names:
                # No reverse accessor or already declared. Note that this would also leave any
                # explicitly declared(i.e. non-inferred) reverse accessors alone
                continue

            related_model_cls = self.django_context.get_field_related_model_cls(relation)

            try:
                related_model_info = self.lookup_class_typeinfo_or_incomplete_defn_error(related_model_cls)
            except helpers.IncompleteDefnException as exc:
                if not self.api.final_iteration:
                    raise exc
                else:
                    continue

            if isinstance(relation, OneToOneRel):
                self.add_new_node_to_model_class(
                    attname,
                    Instance(
                        reverse_one_to_one_descriptor,
                        [Instance(self.model_classdef.info, []), Instance(related_model_info, [])],
                    ),
                )
                continue

            if isinstance(relation, ForeignObjectRel):
                related_manager_info = None
                try:
                    related_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(
                        fullnames.RELATED_MANAGER_CLASS
                    )
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
                    if fallback_manager is not None:
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
                            Var("kwargs", AnyType(TypeOfAny.implementation_artifact)),
                            AnyType(TypeOfAny.implementation_artifact),
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
                            Var("kwargs", AnyType(TypeOfAny.implementation_artifact)),
                            AnyType(TypeOfAny.implementation_artifact),
                            initializer=None,
                            kind=ARG_STAR2,
                        )
                    ],
                    return_type=return_type,
                )


class ProcessManyToManyFields(ModelClassInitializer):
    """
    Processes 'ManyToManyField()' fields and generates any implicit through tables that
    Django also generates. It won't do anything if the model is abstract or for fields
    where an explicit 'through' argument has been passed.
    """

    def run(self) -> None:
        if self.is_model_abstract:
            # TODO: Create abstract through models?
            return

        # Start out by prefetching a couple of dependencies needed to be able to declare any
        # new, implicit, through model class.
        model_base = self.lookup_typeinfo(fullnames.MODEL_CLASS_FULLNAME)
        fk_field = self.lookup_typeinfo(fullnames.FOREIGN_KEY_FULLNAME)
        manager_info = self.lookup_typeinfo(fullnames.MANAGER_CLASS_FULLNAME)
        if model_base is None or fk_field is None or manager_info is None:
            raise helpers.IncompleteDefnException()

        from_pk = self.get_pk_instance(self.model_classdef.info)
        fk_set_type, fk_get_type = get_field_descriptor_types(fk_field, is_set_nullable=False, is_get_nullable=False)

        for defn in self.model_classdef.defs.body:
            # Check if this part of the class body is an assignment from a 'ManyToManyField' call
            # <field> = ManyToManyField(...)
            if (
                isinstance(defn, AssignmentStmt)
                and len(defn.lvalues) == 1
                and isinstance(defn.lvalues[0], NameExpr)
                and isinstance(defn.rvalue, CallExpr)
                and len(defn.rvalue.args) > 0  # Need at least the 'to' argument
                and isinstance(defn.rvalue.callee, RefExpr)
                and isinstance(defn.rvalue.callee.node, TypeInfo)
                and defn.rvalue.callee.node.has_base(fullnames.MANYTOMANY_FIELD_FULLNAME)
            ):
                m2m_field_name = defn.lvalues[0].name
                m2m_field_symbol = self.model_classdef.info.names.get(m2m_field_name)
                # The symbol referred to by the assignment expression is expected to be a variable
                if m2m_field_symbol is None or not isinstance(m2m_field_symbol.node, Var):
                    continue
                # Resolve argument information of the 'ManyToManyField(...)' call
                args = self.resolve_many_to_many_arguments(defn.rvalue, context=defn)
                if (
                    # Ignore calls without required 'to' argument, mypy will complain
                    args is None
                    or not isinstance(args.to.model, Instance)
                    # Call has explicit 'through=', no need to create any implicit through table
                    or args.through is not None
                ):
                    continue

                # Get the names of the implicit through model that will be generated
                through_model_name = f"{self.model_classdef.name}_{m2m_field_name}"
                through_model_fullname = f"{self.model_classdef.info.module_name}.{through_model_name}"
                # If implicit through model is already declared there's nothing more we should do
                through_model = self.lookup_typeinfo(through_model_fullname)
                if through_model is not None:
                    continue
                # Declare a new, empty, implicitly generated through model class named: '<Model>_<field_name>'
                through_model = self.add_new_class_for_current_module(
                    through_model_name, bases=[Instance(model_base, [])]
                )
                # We attempt to be a bit clever here and store the generated through model's fullname in
                # the metadata of the class containing the 'ManyToManyField' call expression, where its
                # identifier is the field name of the 'ManyToManyField'. This would allow the containing
                # model to always find the implicit through model, so that it doesn't get lost.
                model_metadata = helpers.get_django_metadata(self.model_classdef.info)
                model_metadata.setdefault("m2m_throughs", {})
                model_metadata["m2m_throughs"][m2m_field_name] = through_model.fullname
                # Add a 'pk' symbol to the model class
                helpers.add_new_sym_for_info(
                    through_model, name="pk", sym_type=self.default_pk_instance.copy_modified()
                )
                # Add an 'id' symbol to the model class
                helpers.add_new_sym_for_info(
                    through_model, name="id", sym_type=self.default_pk_instance.copy_modified()
                )
                # Add the foreign key to the model containing the 'ManyToManyField' call:
                # <containing_model> or from_<model>
                from_name = (
                    f"from_{self.model_classdef.name.lower()}" if args.to.self else self.model_classdef.name.lower()
                )
                helpers.add_new_sym_for_info(
                    through_model,
                    name=from_name,
                    sym_type=Instance(
                        fk_field,
                        [
                            helpers.convert_any_to_type(fk_set_type, Instance(self.model_classdef.info, [])),
                            helpers.convert_any_to_type(fk_get_type, Instance(self.model_classdef.info, [])),
                        ],
                    ),
                )
                # Add the foreign key's '_id' field: <containing_model>_id or from_<model>_id
                helpers.add_new_sym_for_info(through_model, name=f"{from_name}_id", sym_type=from_pk.copy_modified())
                # Add the foreign key to the model on the opposite side of the relation
                # i.e. the model given as 'to' argument to the 'ManyToManyField' call:
                # <other_model> or to_<model>
                to_name = f"to_{args.to.model.type.name.lower()}" if args.to.self else args.to.model.type.name.lower()
                helpers.add_new_sym_for_info(
                    through_model,
                    name=to_name,
                    sym_type=Instance(
                        fk_field,
                        [
                            helpers.convert_any_to_type(fk_set_type, args.to.model),
                            helpers.convert_any_to_type(fk_get_type, args.to.model),
                        ],
                    ),
                )
                # Add the foreign key's '_id' field: <other_model>_id or to_<model>_id
                other_pk = self.get_pk_instance(args.to.model.type)
                helpers.add_new_sym_for_info(through_model, name=f"{to_name}_id", sym_type=other_pk.copy_modified())
                # Add a manager named 'objects'
                helpers.add_new_sym_for_info(
                    through_model,
                    name="objects",
                    sym_type=Instance(manager_info, [Instance(through_model, [])]),
                )
                # Also add manager as '_default_manager' attribute
                helpers.add_new_sym_for_info(
                    through_model,
                    name="_default_manager",
                    sym_type=Instance(manager_info, [Instance(through_model, [])]),
                )

    @cached_property
    def default_pk_instance(self) -> Instance:
        default_pk_field = self.lookup_typeinfo(self.django_context.settings.DEFAULT_AUTO_FIELD)
        if default_pk_field is None:
            raise helpers.IncompleteDefnException()
        return Instance(
            default_pk_field,
            list(get_field_descriptor_types(default_pk_field, is_set_nullable=True, is_get_nullable=False)),
        )

    def get_pk_instance(self, model: TypeInfo, /) -> Instance:
        """
        Get a primary key instance of provided model's type info. If primary key can't be resolved,
        return a default declaration.
        """
        contains_from_pk_info = model.get_containing_type_info("pk")
        if contains_from_pk_info is not None:
            pk = contains_from_pk_info.names["pk"].node
            if isinstance(pk, Var) and isinstance(pk.type, Instance):
                return pk.type
        return self.default_pk_instance

    def resolve_many_to_many_arguments(self, call: CallExpr, /, context: Context) -> Optional[M2MArguments]:
        """
        Inspect a 'ManyToManyField(...)' call to collect argument data on any 'to' and
        'through' arguments.
        """
        look_for: Dict[str, Optional[Expression]] = {"to": None, "through": None}
        # Look for 'to', being declared as the first positional argument
        if call.arg_kinds[0].is_positional():
            look_for["to"] = call.args[0]
        # Look for 'through', being declared as the sixth positional argument.
        if len(call.args) > 5 and call.arg_kinds[5].is_positional():
            look_for["through"] = call.args[5]

        # Sort out if any of the expected arguments was provided as keyword arguments
        for arg_expr, _arg_kind, arg_name in zip(call.args, call.arg_kinds, call.arg_names):
            if arg_name in look_for and look_for[arg_name] is None:
                look_for[arg_name] = arg_expr

        # 'to' is a required argument of 'ManyToManyField()', we can't do anything if it's not provided
        to_arg = look_for["to"]
        if to_arg is None:
            return None

        # Resolve the type of the 'to' argument expression
        to_model: Optional[ProperType]
        if isinstance(to_arg, StrExpr) and to_arg.value == "self":
            to_model = Instance(self.model_classdef.info, [])
            to_self = True
        else:
            to_model = get_model_from_expression(to_arg, api=self.api, django_context=self.django_context)
            to_self = False
        if to_model is None:
            return None
        to = M2MTo(arg=to_arg, model=to_model, self=to_self)

        # Resolve the type of the 'through' argument expression
        through_arg = look_for["through"]
        through = None
        if through_arg is not None:
            through_model = get_model_from_expression(through_arg, api=self.api, django_context=self.django_context)
            if through_model is not None:
                through = M2MThrough(arg=through_arg, model=through_model)

        return M2MArguments(to=to, through=through)


class MetaclassAdjustments(ModelClassInitializer):
    @classmethod
    def adjust_model_class(cls, ctx: ClassDefContext) -> None:
        """
        For the sake of type checkers other than mypy, some attributes that are
        dynamically added by Django's model metaclass has been annotated on
        `django.db.models.base.Model`. We remove those attributes and will handle them
        through the plugin.
        """
        if ctx.cls.fullname != fullnames.MODEL_CLASS_FULLNAME:
            return

        does_not_exist = ctx.cls.info.names.get("DoesNotExist")
        if does_not_exist is not None and isinstance(does_not_exist.node, Var) and not does_not_exist.plugin_generated:
            del ctx.cls.info.names["DoesNotExist"]

        multiple_objects_returned = ctx.cls.info.names.get("MultipleObjectsReturned")
        if (
            multiple_objects_returned is not None
            and isinstance(multiple_objects_returned.node, Var)
            and not multiple_objects_returned.plugin_generated
        ):
            del ctx.cls.info.names["MultipleObjectsReturned"]

        objects = ctx.cls.info.names.get("objects")
        if objects is not None and isinstance(objects.node, Var) and not objects.plugin_generated:
            del ctx.cls.info.names["objects"]

        return

    def get_exception_bases(self, name: str) -> List[Instance]:
        bases = []
        for model_base in self.model_classdef.info.direct_base_classes():
            exception_base_sym = model_base.names.get(name)
            if (
                # Base class is a Model
                model_base.metaclass_type is not None
                and model_base.metaclass_type.type.fullname == fullnames.MODEL_METACLASS_FULLNAME
                # But base class is not 'models.Model'
                and model_base.fullname != fullnames.MODEL_CLASS_FULLNAME
                # Base class also has a generated exception base e.g. 'DoesNotExist'
                and exception_base_sym is not None
                and exception_base_sym.plugin_generated
                and isinstance(exception_base_sym.node, TypeInfo)
            ):
                bases.append(Instance(exception_base_sym.node, []))

        return bases

    def add_exception_classes(self) -> None:
        """
        Adds exception classes 'DoesNotExist' and 'MultipleObjectsReturned' to a model
        type, aligned with how the model metaclass does it runtime.

        If the model is abstract, exceptions will be added as abstract attributes.
        """
        if "DoesNotExist" not in self.model_classdef.info.names:
            object_does_not_exist = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.OBJECT_DOES_NOT_EXIST)
            does_not_exist: Union[Var, TypeInfo]
            if self.is_model_abstract:
                does_not_exist = self.create_new_var("DoesNotExist", TypeType(Instance(object_does_not_exist, [])))
                does_not_exist.is_abstract_var = True
            else:
                does_not_exist = helpers.create_type_info(
                    "DoesNotExist",
                    self.model_classdef.info.fullname,
                    self.get_exception_bases("DoesNotExist") or [Instance(object_does_not_exist, [])],
                )
            self.model_classdef.info.names[does_not_exist.name] = SymbolTableNode(
                MDEF, does_not_exist, plugin_generated=True
            )

        if "MultipleObjectsReturned" not in self.model_classdef.info.names:
            django_multiple_objects_returned = self.lookup_typeinfo_or_incomplete_defn_error(
                fullnames.MULTIPLE_OBJECTS_RETURNED
            )
            multiple_objects_returned: Union[Var, TypeInfo]
            if self.is_model_abstract:
                multiple_objects_returned = self.create_new_var(
                    "MultipleObjectsReturned", TypeType(Instance(django_multiple_objects_returned, []))
                )
                multiple_objects_returned.is_abstract_var = True
            else:
                multiple_objects_returned = helpers.create_type_info(
                    "MultipleObjectsReturned",
                    self.model_classdef.info.fullname,
                    (
                        self.get_exception_bases("MultipleObjectsReturned")
                        or [Instance(django_multiple_objects_returned, [])]
                    ),
                )
            self.model_classdef.info.names[multiple_objects_returned.name] = SymbolTableNode(
                MDEF, multiple_objects_returned, plugin_generated=True
            )

    def run(self) -> None:
        self.add_exception_classes()


def process_model_class(ctx: ClassDefContext, django_context: DjangoContext) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultPrimaryKey,
        AddPrimaryKeyAlias,
        AddRelatedModelsId,
        AddManagers,
        AddDefaultManagerAttribute,
        AddReverseLookups,
        AddExtraFieldMethods,
        ProcessManyToManyFields,
        MetaclassAdjustments,
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

    assert isinstance(ctx.api, TypeAnalyser)
    assert isinstance(ctx.api.api, SemanticAnalyzer)
    return get_or_create_annotated_type(ctx.api.api, type_arg, fields_dict=fields_dict)


def get_or_create_annotated_type(
    api: Union[SemanticAnalyzer, CheckerPluginInterface], model_type: Instance, fields_dict: Optional[TypedDictType]
) -> ProperType:
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
        model_module_file = api.modules.get(model_module_name)  # type: ignore[union-attr]
        if model_module_file is None:
            return AnyType(TypeOfAny.from_error)

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
