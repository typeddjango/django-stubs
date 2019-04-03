from mypy.plugin import ClassDefContext, MethodContext
from mypy.types import CallableType, Instance, NoneTyp, Type, TypeType

from mypy_django_plugin import helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def extract_proper_type_for_get_form(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    form_class_type = helpers.get_argument_type_by_name(ctx, 'form_class')
    if form_class_type is None or isinstance(form_class_type, NoneTyp):
        # extract from specified form_class in metadata
        form_class_fullname = helpers.get_django_metadata(object_type.type).get('form_class', None)
        if not form_class_fullname:
            return ctx.default_return_type

        return ctx.api.named_generic_type(form_class_fullname, [])

    if isinstance(form_class_type, TypeType) and isinstance(form_class_type.item, Instance):
        return form_class_type.item

    if isinstance(form_class_type, CallableType) and isinstance(form_class_type.ret_type, Instance):
        return form_class_type.ret_type

    return ctx.default_return_type


def extract_proper_type_for_get_form_class(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    form_class_fullname = helpers.get_django_metadata(object_type.type).get('form_class', None)
    if not form_class_fullname:
        return ctx.default_return_type

    return TypeType(ctx.api.named_generic_type(form_class_fullname, []))
