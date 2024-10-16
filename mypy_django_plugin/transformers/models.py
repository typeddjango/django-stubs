from collections import deque
from functools import cached_property
from typing import Any, Dict, Iterable, List, Optional, Type, Union, cast

from django.db.models import Manager, Model
from django.db.models.fields import DateField, DateTimeField, Field
from django.db.models.fields.reverse_related import ForeignObjectRel, ManyToManyRel, OneToOneRel
from mypy.checker import TypeChecker
from mypy.nodes import (
    ARG_STAR2,
    MDEF,
    Argument,
    AssignmentStmt,
    CallExpr,
    Context,
    Expression,
    FakeInfo,
    NameExpr,
    RefExpr,
    Statement,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import AnalyzeTypeContext, AttributeContext, ClassDefContext
from mypy.plugins import common
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import TypeAnalyser
from mypy.types import (
    AnyType,
    ExtraAttrs,
    Instance,
    ProperType,
    TypedDictType,
    TypeOfAny,
    TypeType,
    TypeVarType,
    get_proper_type,
)
from mypy.types import Type as MypyType
from mypy.typevars import fill_typevars, fill_typevars_with_any

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.errorcodes import MANAGER_MISSING
from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.lib.fullnames import ANNOTATIONS_FULLNAME
from mypy_django_plugin.transformers.fields import FieldDescriptorTypes, get_field_descriptor_types
from mypy_django_plugin.transformers.managers import (
    MANAGER_METHODS_RETURNING_QUERYSET,
    create_manager_info_from_from_queryset_call,
)
from mypy_django_plugin.transformers.manytomany import M2MArguments, M2MThrough, M2MTo


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

    def get_or_create_manager_with_any_fallback(self) -> Optional[TypeInfo]:
        """
        Create a Manager subclass with fallback to Any for unknown attributes
        and methods. This is used for unresolved managers, where we don't know
        the actual type of the manager.

        The created class is reused if multiple unknown managers are encountered.
        """

        name = "UnknownManager"

        # Check if we've already created a fallback manager class for this
        # module, and if so reuse that.
        manager_info = self.lookup_typeinfo(f"{self.model_classdef.info.module_name}.{name}")
        if manager_info and manager_info.metadata.get("django", {}).get("any_fallback_manager"):
            return manager_info

        fallback_queryset = self.get_or_create_queryset_with_any_fallback()
        if fallback_queryset is None:
            return None
        base_manager_fullname = fullnames.MANAGER_CLASS_FULLNAME
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


class AddAnnotateUtilities(ModelClassInitializer):
    """
    Creates a model subclass that will be used when the model's manager/queryset calls
    'annotate' to hold on to attributes that Django adds to a model instance.

    Example:

        class MyModel(models.Model):
            ...

        class MyModel@AnnotatedWith(MyModel, django_stubs_ext.Annotations[_Annotations]):
            ...
    """

    def run(self) -> None:
        annotations = self.lookup_typeinfo_or_incomplete_defn_error("django_stubs_ext.Annotations")
        object_does_not_exist = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.OBJECT_DOES_NOT_EXIST)
        multiple_objects_returned = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.MULTIPLE_OBJECTS_RETURNED)
        annotated_model_name = self.model_classdef.info.name + "@AnnotatedWith"
        annotated_model = self.lookup_typeinfo(self.model_classdef.info.module_name + "." + annotated_model_name)
        if annotated_model is None:
            model_type = fill_typevars_with_any(self.model_classdef.info)
            assert isinstance(model_type, Instance)
            annotations_type = fill_typevars(annotations)
            assert isinstance(annotations_type, Instance)
            annotated_model = self.add_new_class_for_current_module(
                annotated_model_name, bases=[model_type, annotations_type]
            )
            annotated_model.defn.type_vars = annotations.defn.type_vars
            annotated_model.add_type_vars()
            helpers.mark_as_annotated_model(annotated_model)
            if self.is_model_abstract:
                # Below are abstract attributes, and in a stub file mypy requires
                # explicit ABCMeta if not all abstract attributes are implemented i.e.
                # class is kept abstract. So we add the attributes to get mypy off our
                # back
                helpers.add_new_sym_for_info(
                    annotated_model, "DoesNotExist", TypeType(Instance(object_does_not_exist, []))
                )
                helpers.add_new_sym_for_info(
                    annotated_model, "MultipleObjectsReturned", TypeType(Instance(multiple_objects_returned, []))
                )


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
        manager_type = helpers.fill_manager(manager_info, Instance(self.model_classdef.info, []))
        self.add_new_node_to_model_class(manager_name, manager_type, is_classvar=True)

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        manager_info: Optional[TypeInfo]

        incomplete_manager_defs = set()
        for manager_name, manager in model_cls._meta.managers_map.items():
            manager_node = self.model_classdef.info.get(manager_name)
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

            assert self.model_classdef.info.self_type is not None
            manager_type = helpers.fill_manager(manager_info, self.model_classdef.info.self_type)
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
                    assert self.model_classdef.info.self_type is not None
                    manager_type = helpers.fill_manager(fallback_manager_info, self.model_classdef.info.self_type)
                    self.add_new_node_to_model_class(manager_name, manager_type, is_classvar=True)

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

        default_manager = helpers.fill_manager(default_manager_info, Instance(self.model_classdef.info, []))
        self.add_new_node_to_model_class("_default_manager", default_manager, is_classvar=True)


class AddReverseLookups(ModelClassInitializer):
    @cached_property
    def reverse_one_to_one_descriptor(self) -> TypeInfo:
        return self.lookup_typeinfo_or_incomplete_defn_error(fullnames.REVERSE_ONE_TO_ONE_DESCRIPTOR)

    @cached_property
    def reverse_many_to_one_descriptor(self) -> TypeInfo:
        return self.lookup_typeinfo_or_incomplete_defn_error(fullnames.REVERSE_MANY_TO_ONE_DESCRIPTOR)

    @cached_property
    def many_to_many_descriptor(self) -> TypeInfo:
        return self.lookup_typeinfo_or_incomplete_defn_error(fullnames.MANY_TO_MANY_DESCRIPTOR)

    def process_relation(self, relation: ForeignObjectRel) -> None:
        attname = relation.get_accessor_name()
        if attname is None:
            # No reverse accessor.
            return

        to_model_cls = self.django_context.get_field_related_model_cls(relation)
        to_model_info = self.lookup_class_typeinfo_or_incomplete_defn_error(to_model_cls)

        reverse_lookup_declared = attname in self.model_classdef.info.names
        if isinstance(relation, OneToOneRel):
            if not reverse_lookup_declared:
                self.add_new_node_to_model_class(
                    attname,
                    Instance(
                        self.reverse_one_to_one_descriptor,
                        [Instance(self.model_classdef.info, []), Instance(to_model_info, [])],
                    ),
                )
            return
        elif isinstance(relation, ManyToManyRel):
            if not reverse_lookup_declared:
                # TODO: 'relation' should be based on `TypeInfo` instead of Django runtime.
                assert relation.through is not None
                through_fullname = helpers.get_class_fullname(relation.through)
                through_model_info = self.lookup_typeinfo_or_incomplete_defn_error(through_fullname)
                self.add_new_node_to_model_class(
                    attname,
                    Instance(
                        self.many_to_many_descriptor, [Instance(to_model_info, []), Instance(through_model_info, [])]
                    ),
                    is_classvar=True,
                )
            return
        elif not reverse_lookup_declared:
            # ManyToOneRel
            self.add_new_node_to_model_class(
                attname, Instance(self.reverse_many_to_one_descriptor, [Instance(to_model_info, [])]), is_classvar=True
            )

        related_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(fullnames.RELATED_MANAGER_CLASS)
        # TODO: Support other reverse managers than `_default_manager`
        default_manager = to_model_info.names.get("_default_manager")
        if default_manager is None:
            if not self.api.final_iteration:
                raise helpers.IncompleteDefnException()
            # When we get no default manager we can't customize the reverse manager any
            # further and will just fall back to the manager declared on the descriptor.
            # If a django model has a Manager class that cannot be resolved statically
            # (if it is generated in a way where we cannot import it, like
            # `objects = my_manager_factory()`)
            #
            # See https://github.com/typeddjango/django-stubs/pull/993
            # for more information on when this error can occur.
            self.ctx.api.fail(
                (
                    f"Couldn't resolve related manager {attname!r} for relation "
                    f"'{to_model_info.fullname}.{relation.field.name}'."
                ),
                self.ctx.cls,
                code=MANAGER_MISSING,
            )
            return

        default_manager_type = get_proper_type(default_manager.type)
        if (
            # '_default_manager' attribute is a node type we can't process
            not isinstance(default_manager_type, Instance)
            # Already has a related manager subclassed from the default manager
            or helpers.get_reverse_manager_info(self.api, model_info=to_model_info, derived_from="_default_manager")
            is not None
            # When the default manager isn't custom there's no need to create a new type
            # as `RelatedManager` has `models.Manager` as base
            or default_manager_type.type.fullname == fullnames.MANAGER_CLASS_FULLNAME
        ):
            return

        # Create a reverse manager subclassed from the default manager of the related
        # model and 'RelatedManager'
        related_manager = Instance(related_manager_info, [Instance(to_model_info, [])])
        # The reverse manager is based on the related model's manager, so it makes most sense to add the new
        # related manager in that module
        new_related_manager_info = helpers.add_new_class_for_module(
            module=self.api.modules[to_model_info.module_name],
            name=f"{to_model_info.name}_RelatedManager",
            bases=[related_manager, default_manager_type],
        )
        # Stash the new reverse manager type fullname on the related model, so we don't duplicate
        # or have to create it again for other reverse relations
        helpers.set_reverse_manager_info(
            to_model_info,
            derived_from="_default_manager",
            fullname=new_related_manager_info.fullname,
        )

    def run_with_model_cls(self, model_cls: Type[Model]) -> None:
        # add related managers etc.
        processing_incomplete = False
        for relation in self.django_context.get_model_relations(model_cls):
            try:
                self.process_relation(relation)
            except helpers.IncompleteDefnException:
                processing_incomplete = True

        if processing_incomplete and not self.api.final_iteration:
            raise helpers.IncompleteDefnException


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
    Processes 'ManyToManyField()' fields and;

    - Generates any implicit through tables that Django also generates. It won't do
      anything if the model is abstract or for fields where an explicit 'through'
      argument has been passed.
    - Creates related managers for both ends of the many to many relationship

    TODO: Move the 'related_name' contribution from 'AddReverseLookups' to here. As it
          makes sense to add it when processing ManyToManyField
    """

    def statements(self) -> Iterable[Statement]:
        """
        Returns class body statements from the current model and any of its bases that
        is an abstract model. Statements from any concrete parent class or parents of
        that concrete class will be skipped.
        """
        processed_models = set()
        # Produce all statements from current class
        model_bases = deque([self.model_classdef])
        # Do a breadth first search over the current model and its bases, to find all
        # abstract parent models that have not been "interrupted" by any concrete model.
        while model_bases:
            model = model_bases.popleft()
            yield from model.defs.body
            if isinstance(model.info, FakeInfo):
                # While loading from cache ClassDef infos are faked and 'FakeInfo' doesn't have
                # all attributes of a 'TypeInfo' set. See #2184
                continue
            for base in model.info.bases:
                # Only produce any additional statements from abstract model bases, as they
                # simulate regular python inheritance. Avoid concrete models, and any of their
                # parents, as they're handled differently by Django.
                if helpers.is_abstract_model(base.type) and base.type.fullname not in processed_models:
                    model_bases.append(base.type.defn)
                    processed_models.add(base.type.fullname)

    def run(self) -> None:
        if self.is_model_abstract:
            # TODO: Create abstract through models?
            return

        for statement in self.statements():
            # Check if this part of the class body is an assignment from a 'ManyToManyField' call
            # <field> = ManyToManyField(...)
            if (
                isinstance(statement, AssignmentStmt)
                and len(statement.lvalues) == 1
                and isinstance(statement.lvalues[0], NameExpr)
                and isinstance(statement.rvalue, CallExpr)
                and len(statement.rvalue.args) > 0  # Need at least the 'to' argument
                and isinstance(statement.rvalue.callee, RefExpr)
                and isinstance(statement.rvalue.callee.node, TypeInfo)
                and statement.rvalue.callee.node.has_base(fullnames.MANYTOMANY_FIELD_FULLNAME)
            ):
                m2m_field_name = statement.lvalues[0].name
                m2m_field_symbol = self.model_classdef.info.get(m2m_field_name)
                # The symbol referred to by the assignment expression is expected to be a variable
                if m2m_field_symbol is None or not isinstance(m2m_field_symbol.node, Var):
                    continue
                # Resolve argument information of the 'ManyToManyField(...)' call
                args = self.resolve_many_to_many_arguments(statement.rvalue, context=statement)
                # Ignore calls without required 'to' argument, mypy will complain
                if args is None:
                    continue
                # Get the names of the implicit through model that will be generated
                through_model_name = f"{self.model_classdef.name}_{m2m_field_name}"
                through_model = self.create_through_table_class(
                    field_name=m2m_field_name,
                    model_name=through_model_name,
                    model_fullname=f"{self.model_classdef.info.module_name}.{through_model_name}",
                    m2m_args=args,
                )
                container = self.model_classdef.info.get_containing_type_info(m2m_field_name)
                if (
                    through_model is not None
                    and container is not None
                    and container.fullname != self.model_classdef.info.fullname
                    and helpers.is_abstract_model(container)
                ):
                    # ManyToManyField is inherited from an abstract parent class, so in
                    # order to get the to and the through model argument right we
                    # override the ManyToManyField attribute on the current class
                    helpers.add_new_sym_for_info(
                        self.model_classdef.info,
                        name=m2m_field_name,
                        sym_type=Instance(self.m2m_field, [args.to.model, Instance(through_model, [])]),
                    )
                # Create a 'ManyRelatedManager' class for the processed model
                self.create_many_related_manager(Instance(self.model_classdef.info, []))
                if isinstance(args.to.model, Instance):
                    # Create a 'ManyRelatedManager' class for the related model
                    self.create_many_related_manager(args.to.model)

    @cached_property
    def default_pk_instance(self) -> Instance:
        default_pk_field = self.lookup_typeinfo(self.django_context.settings.DEFAULT_AUTO_FIELD)
        if default_pk_field is None:
            raise helpers.IncompleteDefnException()
        return Instance(
            default_pk_field,
            list(get_field_descriptor_types(default_pk_field, is_set_nullable=True, is_get_nullable=False)),
        )

    @cached_property
    def model_pk_instance(self) -> Instance:
        return self.get_pk_instance(self.model_classdef.info)

    @cached_property
    def model_base(self) -> TypeInfo:
        info = self.lookup_typeinfo(fullnames.MODEL_CLASS_FULLNAME)
        if info is None:
            raise helpers.IncompleteDefnException()
        return info

    @cached_property
    def fk_field(self) -> TypeInfo:
        info = self.lookup_typeinfo(fullnames.FOREIGN_KEY_FULLNAME)
        if info is None:
            raise helpers.IncompleteDefnException()
        return info

    @cached_property
    def m2m_field(self) -> TypeInfo:
        info = self.lookup_typeinfo(fullnames.MANYTOMANY_FIELD_FULLNAME)
        if info is None:
            raise helpers.IncompleteDefnException()
        return info

    @cached_property
    def manager_info(self) -> TypeInfo:
        info = self.lookup_typeinfo(fullnames.MANAGER_CLASS_FULLNAME)
        if info is None:
            raise helpers.IncompleteDefnException()
        return info

    @cached_property
    def fk_field_types(self) -> FieldDescriptorTypes:
        return get_field_descriptor_types(self.fk_field, is_set_nullable=False, is_get_nullable=False)

    @cached_property
    def many_related_manager(self) -> TypeInfo:
        return self.lookup_typeinfo_or_incomplete_defn_error(fullnames.MANY_RELATED_MANAGER)

    def get_pk_instance(self, model: TypeInfo, /) -> Instance:
        """
        Get a primary key instance of provided model's type info. If primary key can't be resolved,
        return a default declaration.
        """
        contains_from_pk_info = model.get_containing_type_info("pk")
        if contains_from_pk_info is not None:
            pk = contains_from_pk_info.names["pk"].node
            if isinstance(pk, Var):
                pk_type = get_proper_type(pk.type)
                if isinstance(pk_type, Instance):
                    return pk_type
        return self.default_pk_instance

    def create_through_table_class(
        self, field_name: str, model_name: str, model_fullname: str, m2m_args: M2MArguments
    ) -> Optional[TypeInfo]:
        if not isinstance(m2m_args.to.model, Instance):
            return None
        elif m2m_args.through is not None:
            # Call has explicit 'through=', no need to create any implicit through table
            return m2m_args.through.model.type if isinstance(m2m_args.through.model, Instance) else None

        # If through model is already declared there's nothing more we should do
        through_model = self.lookup_typeinfo(model_fullname)
        if through_model is not None:
            return through_model
        # Declare a new, empty, implicitly generated through model class named: '<Model>_<field_name>'
        through_model = self.add_new_class_for_current_module(model_name, bases=[Instance(self.model_base, [])])
        # We attempt to be a bit clever here and store the generated through model's fullname in
        # the metadata of the class containing the 'ManyToManyField' call expression, where its
        # identifier is the field name of the 'ManyToManyField'. This would allow the containing
        # model to always find the implicit through model, so that it doesn't get lost.
        model_metadata = helpers.get_django_metadata(self.model_classdef.info)
        model_metadata.setdefault("m2m_throughs", {})
        model_metadata["m2m_throughs"][field_name] = through_model.fullname
        # Add a 'pk' symbol to the model class
        helpers.add_new_sym_for_info(through_model, name="pk", sym_type=self.default_pk_instance.copy_modified())
        # Add an 'id' symbol to the model class
        helpers.add_new_sym_for_info(through_model, name="id", sym_type=self.default_pk_instance.copy_modified())
        # Add the foreign key to the model containing the 'ManyToManyField' call:
        # <containing_model> or from_<model>
        from_name = f"from_{self.model_classdef.name.lower()}" if m2m_args.to.self else self.model_classdef.name.lower()
        helpers.add_new_sym_for_info(
            through_model,
            name=from_name,
            sym_type=Instance(
                self.fk_field,
                [
                    helpers.convert_any_to_type(self.fk_field_types.set, Instance(self.model_classdef.info, [])),
                    helpers.convert_any_to_type(self.fk_field_types.get, Instance(self.model_classdef.info, [])),
                ],
            ),
        )
        # Add the foreign key's '_id' field: <containing_model>_id or from_<model>_id
        helpers.add_new_sym_for_info(
            through_model, name=f"{from_name}_id", sym_type=self.model_pk_instance.copy_modified()
        )
        # Add the foreign key to the model on the opposite side of the relation
        # i.e. the model given as 'to' argument to the 'ManyToManyField' call:
        # <other_model> or to_<model>
        to_name = (
            f"to_{m2m_args.to.model.type.name.lower()}" if m2m_args.to.self else m2m_args.to.model.type.name.lower()
        )
        helpers.add_new_sym_for_info(
            through_model,
            name=to_name,
            sym_type=Instance(
                self.fk_field,
                [
                    helpers.convert_any_to_type(self.fk_field_types.set, m2m_args.to.model),
                    helpers.convert_any_to_type(self.fk_field_types.get, m2m_args.to.model),
                ],
            ),
        )
        # Add the foreign key's '_id' field: <other_model>_id or to_<model>_id
        other_pk = self.get_pk_instance(m2m_args.to.model.type)
        helpers.add_new_sym_for_info(through_model, name=f"{to_name}_id", sym_type=other_pk.copy_modified())
        # Add a manager named 'objects'
        helpers.add_new_sym_for_info(
            through_model,
            name="objects",
            sym_type=Instance(self.manager_info, [Instance(through_model, [])]),
            is_classvar=True,
        )
        # Also add manager as '_default_manager' attribute
        helpers.add_new_sym_for_info(
            through_model,
            name="_default_manager",
            sym_type=Instance(self.manager_info, [Instance(through_model, [])]),
            is_classvar=True,
        )
        return through_model

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
        to_model = helpers.get_model_from_expression(
            to_arg, self_model=self.model_classdef.info, api=self.api, django_context=self.django_context
        )
        if to_model is None:
            return None
        to = M2MTo(
            arg=to_arg,
            model=to_model,
            self=to_model.type == self.model_classdef.info,
        )

        # Resolve the type of the 'through' argument expression
        through_arg = look_for["through"]
        through = None
        if through_arg is not None:
            through_model = helpers.get_model_from_expression(
                through_arg, self_model=self.model_classdef.info, api=self.api, django_context=self.django_context
            )
            if through_model is not None:
                through = M2MThrough(arg=through_arg, model=through_model)

        return M2MArguments(to=to, through=through)

    def create_many_related_manager(self, model: Instance) -> None:
        """
        Creates a generic manager that subclasses both 'ManyRelatedManager' and the
        default manager of the given model. These are normally used on both models
        involved in a ManyToManyField.

        The manager classes are generic over a '_Through' model, meaning that they can
        be reused for multiple many to many relations.
        """
        if helpers.get_many_to_many_manager_info(self.api, to=model.type, derived_from="_default_manager") is not None:
            return

        default_manager_node = model.type.names.get("_default_manager")
        if default_manager_node is None:
            raise helpers.IncompleteDefnException()
        default_manager_type = get_proper_type(default_manager_node.type)
        if not isinstance(default_manager_type, Instance):
            return

        # Create a reusable generic subclass that is generic over a 'through' model,
        # explicitly declared it'd could have looked something like below
        #
        # class X(models.Model): ...
        # _Through = TypeVar("_Through", bound=models.Model)
        # class X_ManyRelatedManager(ManyRelatedManager[X, _Through], type(X._default_manager), Generic[_Through]): ...
        through_type_var = self.many_related_manager.defn.type_vars[1]
        assert isinstance(through_type_var, TypeVarType)
        generic_to_many_related_manager = Instance(self.many_related_manager, [model, through_type_var.copy_modified()])
        related_manager_info = helpers.add_new_class_for_module(
            module=self.api.modules[model.type.module_name],
            name=f"{model.type.name}_ManyRelatedManager",
            bases=[generic_to_many_related_manager, default_manager_type],
        )
        # Reuse the '_Through' `TypeVar` from `ManyRelatedManager` in our subclass
        related_manager_info.defn.type_vars = [through_type_var.copy_modified()]
        related_manager_info.add_type_vars()
        # Track the existence of our manager subclass, by tying it to the model it
        # operates on
        helpers.set_many_to_many_manager_info(
            to=model.type, derived_from="_default_manager", manager_info=related_manager_info
        )
        helpers.set_manager_to_model(related_manager_info, model.type)


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
                helpers.is_model_type(model_base)
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
        AddAnnotateUtilities,
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


def handle_annotated_type(ctx: AnalyzeTypeContext, fullname: str) -> MypyType:
    """
    Replaces the 'WithAnnotations' type with a type that can represent an annotated
    model.
    """
    is_with_annotations = fullname == fullnames.WITH_ANNOTATIONS_FULLNAME
    args = ctx.type.args
    if not args:
        return AnyType(TypeOfAny.from_omitted_generics) if is_with_annotations else ctx.type
    type_arg = get_proper_type(ctx.api.analyze_type(args[0]))
    if not isinstance(type_arg, Instance) or not helpers.is_model_type(type_arg.type):
        return type_arg

    fields_dict = None
    if len(args) > 1:
        second_arg_type = get_proper_type(ctx.api.analyze_type(args[1]))
        if isinstance(second_arg_type, TypedDictType) and is_with_annotations:
            fields_dict = second_arg_type
        elif isinstance(second_arg_type, Instance) and second_arg_type.type.fullname == ANNOTATIONS_FULLNAME:
            annotations_type_arg = get_proper_type(second_arg_type.args[0])
            if isinstance(annotations_type_arg, TypedDictType):
                fields_dict = annotations_type_arg
            elif not isinstance(annotations_type_arg, AnyType):
                ctx.api.fail("Only TypedDicts are supported as type arguments to Annotations", ctx.context)
            elif annotations_type_arg.type_of_any == TypeOfAny.from_omitted_generics:
                ctx.api.fail("Missing required TypedDict parameter for generic type Annotations", ctx.context)

    if fields_dict is None:
        return type_arg

    assert isinstance(ctx.api, TypeAnalyser)
    assert isinstance(ctx.api.api, SemanticAnalyzer)
    return get_annotated_type(ctx.api.api, type_arg, fields_dict=fields_dict)


def get_annotated_type(
    api: Union[SemanticAnalyzer, TypeChecker], model_type: Instance, fields_dict: TypedDictType
) -> ProperType:
    """
    Get a model type that can be used to represent an annotated model
    """
    if model_type.extra_attrs:
        extra_attrs = ExtraAttrs(
            attrs={**model_type.extra_attrs.attrs, **(fields_dict.items if fields_dict is not None else {})},
            immutable=model_type.extra_attrs.immutable.copy(),
            mod_name=None,
        )
    else:
        extra_attrs = ExtraAttrs(
            attrs=fields_dict.items if fields_dict is not None else {},
            immutable=None,
            mod_name=None,
        )

    annotated_model: Optional[TypeInfo]
    if helpers.is_annotated_model(model_type.type):
        annotated_model = model_type.type
        if model_type.args:
            annotations = get_proper_type(model_type.args[0])
            if isinstance(annotations, TypedDictType):
                fields_dict = helpers.make_typeddict(
                    api,
                    fields={**annotations.items, **fields_dict.items},
                    required_keys={*annotations.required_keys, *fields_dict.required_keys},
                    readonly_keys={*annotations.readonly_keys, *fields_dict.readonly_keys},
                )
    else:
        annotated_model = helpers.lookup_fully_qualified_typeinfo(api, model_type.type.fullname + "@AnnotatedWith")

    if annotated_model is None:
        return model_type
    return Instance(annotated_model, [fields_dict], extra_attrs=extra_attrs)
