from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, cast

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import AutoField
from django.db.models.fields.related import RelatedField
from mypy.nodes import AssignmentStmt, NameExpr, TypeInfo
from mypy.typeanal import make_optional_type
from mypy.types import AnyType, Instance, NoneType, ProperType, TypeOfAny, UninhabitedType, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers import manytomany

if TYPE_CHECKING:
    from django.db.models.options import _AnyField
    from mypy.checker import TypeChecker
    from mypy.plugin import FunctionContext
    from mypy.semanal import SemanticAnalyzer

    from mypy_django_plugin.django.context import DjangoContext


def _get_current_field_from_assignment(ctx: FunctionContext, django_context: DjangoContext) -> _AnyField | None:
    outer_model_info = helpers.get_typechecker_api(ctx).scope.active_class()
    if outer_model_info is None or not helpers.is_model_type(outer_model_info):
        return None

    field_name = None
    for stmt in outer_model_info.defn.defs.body:
        if isinstance(stmt, AssignmentStmt):
            if stmt.rvalue == ctx.context:
                if not isinstance(stmt.lvalues[0], NameExpr):
                    return None
                field_name = stmt.lvalues[0].name
                break
    if field_name is None:
        return None

    model_cls = django_context.get_model_class_by_fullname(outer_model_info.fullname)
    if model_cls is None:
        return None

    try:
        return model_cls._meta.get_field(field_name)
    except FieldDoesNotExist:
        return None


def fill_descriptor_types_for_related_field(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    current_field = _get_current_field_from_assignment(ctx, django_context)
    if current_field is None:
        return AnyType(TypeOfAny.from_error)

    assert isinstance(current_field, RelatedField)

    try:
        related_model_cls = django_context.get_field_related_model_cls(current_field)
    except UnregisteredModelError:
        return AnyType(TypeOfAny.from_error)

    default_related_field_type = set_descriptor_types_for_field(ctx)
    if len(default_related_field_type.args) != 2:
        return default_related_field_type

    # self reference with abstract=True on the model where ForeignKey is defined
    current_model_cls = current_field.model
    if current_model_cls._meta.abstract and current_model_cls == related_model_cls:
        # for all derived non-abstract classes, set variable with this name to
        # __get__/__set__ of ForeignKey of derived model
        for model_cls in django_context.all_registered_model_classes:
            if issubclass(model_cls, current_model_cls) and not model_cls._meta.abstract:
                derived_model_info = helpers.lookup_class_typeinfo(helpers.get_typechecker_api(ctx), model_cls)
                if derived_model_info is not None:
                    fk_ref_type = helpers.model_instance(derived_model_info)
                    derived_fk_type = helpers.reparametrize_field_type(
                        default_related_field_type, set_type=fk_ref_type, get_type=fk_ref_type
                    )
                    helpers.add_new_sym_for_info(derived_model_info, name=current_field.name, sym_type=derived_fk_type)

    related_model = related_model_cls
    related_model_to_set = related_model_cls
    if related_model_to_set._meta.proxy_for_model is not None:
        related_model_to_set = related_model_to_set._meta.proxy_for_model

    typechecker_api = helpers.get_typechecker_api(ctx)

    related_model_info = helpers.lookup_class_typeinfo(typechecker_api, related_model)
    related_model_type: ProperType
    if related_model_info is None:
        # maybe no type stub
        related_model_type = AnyType(TypeOfAny.unannotated)
    else:
        related_model_type = helpers.model_instance(related_model_info)

    related_model_to_set_info = helpers.lookup_class_typeinfo(typechecker_api, related_model_to_set)
    related_model_to_set_type: ProperType
    if related_model_to_set_info is None:
        # maybe no type stub
        related_model_to_set_type = AnyType(TypeOfAny.unannotated)
    else:
        related_model_to_set_type = helpers.model_instance(related_model_to_set_info)

    # replace Any with referred_to_type
    return helpers.reparametrize_field_type(
        default_related_field_type, set_type=related_model_to_set_type, get_type=related_model_type
    )


class FieldDescriptorTypes(NamedTuple):
    set: MypyType
    get: MypyType


def get_field_descriptor_types(
    field_info: TypeInfo, api: TypeChecker | SemanticAnalyzer, *, is_set_nullable: bool, is_get_nullable: bool
) -> FieldDescriptorTypes:
    """The set/get types a bare `field_info()` call resolves to, from its PEP 696 defaults.

    A subclass that forwards the base type vars without its own defaults (`MyText(TextField[_ST, _GT])`)
    resolves to `Any`, so fall back to the nearest base whose defaults are concrete.
    """
    set_type: MypyType = AnyType(TypeOfAny.from_omitted_generics)
    get_type: MypyType = set_type
    for info in field_info.mro:
        if not info.has_base(fullnames.FIELD_FULLNAME):
            break
        field_args = helpers.get_field_type_args(helpers.fill_field_defaults(info, api))
        if field_args is None:
            break
        if not (isinstance(field_args.set, AnyType) and isinstance(field_args.get, AnyType)):
            set_type, get_type = field_args.set, field_args.get
            break
    if is_set_nullable:
        set_type = make_optional_type(set_type)
    if is_get_nullable:
        get_type = make_optional_type(get_type)
    return FieldDescriptorTypes(set=set_type, get=get_type)


def set_descriptor_types_for_field_callback(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    current_field = _get_current_field_from_assignment(ctx, django_context)
    if current_field is not None:
        if isinstance(current_field, AutoField):
            return set_descriptor_types_for_field(ctx, is_set_nullable=True)

    return set_descriptor_types_for_field(ctx)


def _warn_if_nullable_get_not_optional(ctx: FunctionContext, field_type: Instance) -> None:
    field_args = helpers.get_field_type_args(field_type)
    if field_args is None:
        return
    get_type = field_args.get
    if isinstance(get_type, NoneType) or helpers.is_optional(get_type) or isinstance(get_type, AnyType):
        return
    ctx.api.fail(
        f"{field_type.type.name} is nullable but its generic get type parameter is not optional",
        ctx.context,
    )


def set_descriptor_types_for_field(
    ctx: FunctionContext, *, is_set_nullable: bool = False, is_get_nullable: bool = False
) -> Instance:
    default_return_type = cast("Instance", ctx.default_return_type)
    is_nullable = helpers.get_bool_call_argument_by_name(ctx, "null", default=False)

    if len(default_return_type.args) != 2:
        # A fully bound field (`class F(Field[str, str])`) or a wrapper with its own type parameters
        # (`ArrayField[_ST, _GT, _NullT]`) has no set/get slot to widen: the stub's answer stands.
        if is_nullable:
            _warn_if_nullable_get_not_optional(ctx, default_return_type)
        return default_return_type

    # FileDescriptor.__get__ always returns a FieldFile and its __set__ accepts None; the stub is authoritative.
    if default_return_type.type.has_base(fullnames.FILE_FIELD_FULLNAME):
        return default_return_type

    is_primary_key = helpers.get_bool_call_argument_by_name(ctx, "primary_key", default=False)
    # Allow setting field value to `None` when a field is primary key and has a default that can produce a value
    default_expr = helpers.get_call_argument_by_name(ctx, "default")
    if default_expr is not None:
        is_set_nullable = is_primary_key

    set_type, get_type = get_field_descriptor_types(
        default_return_type.type,
        helpers.get_typechecker_api(ctx),
        is_set_nullable=is_set_nullable or is_nullable,
        is_get_nullable=is_get_nullable or is_nullable,
    )

    # reconcile set and get types with the base field class
    mapped_types = helpers.get_field_type_args(default_return_type)
    assert mapped_types is not None

    # bail if either mapped set or get type is Never
    if not (isinstance(mapped_types.set, UninhabitedType) or isinstance(mapped_types.get, UninhabitedType)):
        # always replace set_type and get_type with (non-Any) mapped types
        set_type = helpers.convert_any_to_type(mapped_types.set, set_type)
        get_type = helpers.convert_any_to_type(mapped_types.get, get_type)
        # The type parameters default to the non-null types, so fold `None` in for nullable fields.
        if is_set_nullable or is_nullable:
            set_type = make_optional_type(set_type)
        if is_get_nullable or is_nullable:
            get_type = make_optional_type(get_type)

    return default_return_type.copy_modified(args=[set_type, get_type])


def transform_into_proper_return_type(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    assert isinstance(default_return_type, Instance)

    outer_model_info = helpers.get_typechecker_api(ctx).scope.active_class()
    if outer_model_info is None or not helpers.is_model_type(outer_model_info):
        return set_descriptor_types_for_field(ctx)

    assert isinstance(outer_model_info, TypeInfo)

    if default_return_type.type.has_base(fullnames.MANYTOMANY_FIELD_FULLNAME):
        return manytomany.fill_model_args_for_many_to_many_field(
            ctx=ctx, model_info=outer_model_info, django_context=django_context
        )
    if default_return_type.type.has_base(fullnames.GENERIC_RELATION_FULLNAME):
        # A to-many relation read through a manager, unlike the foreign keys it shares a base with.
        return default_return_type
    if helpers.has_any_of_bases(default_return_type.type, fullnames.RELATED_FIELDS_CLASSES):
        return fill_descriptor_types_for_related_field(ctx, django_context)

    return set_descriptor_types_for_field_callback(ctx, django_context)
