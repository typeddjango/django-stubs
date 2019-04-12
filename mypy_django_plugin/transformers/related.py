from typing import Optional, Union

from mypy.checkmember import AttributeContext
from mypy.nodes import TypeInfo
from mypy.types import AnyType, Instance, Type, TypeOfAny, UnionType

from mypy_django_plugin import helpers


def _extract_referred_to_type_info(typ: Union[UnionType, Instance]) -> Optional[TypeInfo]:
    if isinstance(typ, Instance):
        return typ.type
    else:
        # should be Union[TYPE, None]
        typ = helpers.make_required(typ)
        if isinstance(typ, Instance):
            return typ.type
    return None


def extract_and_return_primary_key_of_bound_related_field_parameter(ctx: AttributeContext) -> Type:
    if not isinstance(ctx.default_attr_type, Instance) or not (ctx.default_attr_type.type.fullname() == 'builtins.int'):
        return ctx.default_attr_type

    if not isinstance(ctx.type, Instance) or not ctx.type.type.has_base(helpers.MODEL_CLASS_FULLNAME):
        return ctx.default_attr_type

    field_name = ctx.context.name.split('_')[0]
    sym = ctx.type.type.get(field_name)
    if sym and isinstance(sym.type, Instance) and len(sym.type.args) > 0:
        referred_to = sym.type.args[1]
        if isinstance(referred_to, AnyType):
            return AnyType(TypeOfAny.implementation_artifact)

        model_type = _extract_referred_to_type_info(referred_to)
        if model_type is None:
            return AnyType(TypeOfAny.implementation_artifact)

        primary_key_type = helpers.extract_primary_key_type_for_get(model_type)
        if primary_key_type:
            return primary_key_type

    is_nullable = helpers.is_field_nullable(ctx.type.type, field_name)
    if is_nullable:
        return helpers.make_optional(ctx.default_attr_type)

    return ctx.default_attr_type


def determine_type_of_related_manager(ctx: AttributeContext, related_manager_name: str) -> Type:
    if not isinstance(ctx.type, Instance):
        return ctx.default_attr_type

    related_manager_type = helpers.get_related_manager_type_from_metadata(ctx.type.type,
                                                                          related_manager_name, ctx.api)
    if not related_manager_type:
        return ctx.default_attr_type

    return related_manager_type
