from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, cast

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import AutoField
from django.db.models.fields.related import RelatedField
from mypy.nodes import AssignmentStmt, NameExpr, TypeInfo
from mypy.types import AnyType, Instance, NoneType, ProperType, TypeOfAny, UninhabitedType, UnionType, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers import manytomany

if TYPE_CHECKING:
    from django.db.models.options import _AnyField
    from mypy.plugin import FunctionContext

    from mypy_django_plugin.django.context import DjangoContext


def _get_current_field_from_assignment(ctx: FunctionContext, django_context: DjangoContext) -> _AnyField | None:
    outer_model_info = helpers.get_typechecker_api(ctx).scope.active_class()
    if outer_model_info is None or not helpers.is_model_type(outer_model_info):
        return None

    field_name = None
    for stmt in outer_model_info.defn.defs.body:
        if isinstance(stmt, AssignmentStmt) and stmt.rvalue == ctx.context:
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
    field_info: TypeInfo, *, is_set_nullable: bool, is_get_nullable: bool
) -> FieldDescriptorTypes:
    set_type = helpers.get_private_descriptor_type(field_info, "_pyi_private_set_type", is_nullable=is_set_nullable)
    get_type = helpers.get_private_descriptor_type(field_info, "_pyi_private_get_type", is_nullable=is_get_nullable)
    return FieldDescriptorTypes(set=set_type, get=get_type)


def set_descriptor_types_for_field_callback(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    current_field = _get_current_field_from_assignment(ctx, django_context)
    if isinstance(current_field, AutoField):
        return set_descriptor_types_for_field(ctx, is_set_nullable=True)

    return set_descriptor_types_for_field(ctx)


def set_descriptor_types_for_field(
    ctx: FunctionContext, *, is_set_nullable: bool = False, is_get_nullable: bool = False
) -> Instance:
    default_return_type = cast("Instance", ctx.default_return_type)

    is_nullable = helpers.get_bool_call_argument_by_name(ctx, "null", default=False)
    is_primary_key = helpers.get_bool_call_argument_by_name(ctx, "primary_key", default=False)
    # Allow setting field value to `None` when a field is primary key and has a default that can produce a value
    default_expr = helpers.get_call_argument_by_name(ctx, "default")
    if default_expr is not None:
        is_set_nullable = is_primary_key

    set_type, get_type = get_field_descriptor_types(
        default_return_type.type,
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
        get_type = get_proper_type(helpers.convert_any_to_type(mapped_types.get, get_type))

        # the get_type must be optional if the field is nullable
        if (is_get_nullable or is_nullable) and not (
            isinstance(get_type, NoneType) or helpers.is_optional(get_type) or isinstance(get_type, AnyType)
        ):
            ctx.api.fail(
                f"{default_return_type.type.name} is nullable but its generic get type parameter is not optional",
                ctx.context,
            )

    return default_return_type.copy_modified(args=[set_type, get_type])


def determine_type_of_array_field(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = set_descriptor_types_for_field(ctx)

    base_field_arg_type = get_proper_type(helpers.get_call_argument_type_by_name(ctx, "base_field"))
    if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
        return default_return_type

    def drop_combinable(_type: MypyType) -> MypyType | None:
        _type = get_proper_type(_type)
        if isinstance(_type, Instance) and _type.type.has_base(fullnames.COMBINABLE_EXPRESSION_FULLNAME):
            return None
        if isinstance(_type, UnionType):
            items = [reduced for item in _type.items if (reduced := drop_combinable(item)) is not None]
            return UnionType.make_union(items, _type.line, _type.column) if items else None

        return _type

    # Both base_field and return type should derive from Field and thus expect 2 arguments
    assert len(base_field_arg_type.args) == len(default_return_type.args) == 2
    args = []
    for new_type, default_arg in zip(base_field_arg_type.args, default_return_type.args, strict=False):
        # Drop any base_field Combinable type
        reduced = drop_combinable(new_type)
        if reduced is None:
            ctx.api.fail(
                f"Can't have ArrayField expecting {fullnames.COMBINABLE_EXPRESSION_FULLNAME!r} as data type",
                ctx.context,
            )
        else:
            new_type = reduced

        args.append(helpers.convert_any_to_type(default_arg, new_type))

    return default_return_type.copy_modified(args=args)


def fill_model_arg_for_generic_relation(
    ctx: FunctionContext, *, model_info: TypeInfo, django_context: DjangoContext
) -> MypyType:
    """Resolve `GenericRelation("app.Model")` to `GenericRelation[Model]`, as a class reference would."""
    default_return_type = cast("Instance", ctx.default_return_type)
    if not (ctx.args and ctx.args[0] and default_return_type.args):
        return default_return_type
    to_arg = get_proper_type(default_return_type.args[0])
    if not isinstance(to_arg, (UninhabitedType, AnyType)):
        # `GenericRelation(Model)` was already solved from the class reference.
        return default_return_type
    to_model = helpers.get_model_from_expression(
        ctx.args[0][0], self_model=model_info, api=helpers.get_typechecker_api(ctx), django_context=django_context
    )
    if to_model is None:
        return default_return_type
    return default_return_type.copy_modified(args=[to_model])


def transform_into_proper_return_type(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        # A `Field` subclass can be called through a type variable, e.g. `type[F]` where `F` is
        # bound to `Field`. There is no concrete field type to specialize there, and replacing
        # the type variable with its upper bound would widen the result of the call, which is `F`.
        return default_return_type

    outer_model_info = helpers.get_typechecker_api(ctx).scope.active_class()
    if outer_model_info is None or not helpers.is_model_type(outer_model_info):
        if helpers.has_any_of_bases(
            default_return_type.type, (fullnames.MANYTOMANY_FIELD_FULLNAME, fullnames.GENERIC_RELATION_FULLNAME)
        ):
            # Their type args are the related models, not the descriptor set/get types.
            return default_return_type
        return set_descriptor_types_for_field(ctx)

    assert isinstance(outer_model_info, TypeInfo)

    if default_return_type.type.has_base(fullnames.MANYTOMANY_FIELD_FULLNAME):
        return manytomany.fill_model_args_for_many_to_many_field(
            ctx=ctx, model_info=outer_model_info, django_context=django_context
        )
    if default_return_type.type.has_base(fullnames.GENERIC_RELATION_FULLNAME):
        # A to-many relation read through a manager, unlike the foreign keys it shares a base with.
        return fill_model_arg_for_generic_relation(ctx, model_info=outer_model_info, django_context=django_context)
    if helpers.has_any_of_bases(default_return_type.type, fullnames.RELATED_FIELDS_CLASSES):
        return fill_descriptor_types_for_related_field(ctx, django_context)

    if default_return_type.type.has_base(fullnames.ARRAY_FIELD_FULLNAME):
        return determine_type_of_array_field(ctx, django_context)

    return set_descriptor_types_for_field_callback(ctx, django_context)
