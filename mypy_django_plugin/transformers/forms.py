from typing import Optional

from mypy.plugin import MethodContext
from mypy.types import CallableType, Instance, NoneTyp
from mypy.types import Type as MypyType
from mypy.types import TypeType

from mypy_django_plugin.lib import chk_helpers


def get_specified_form_class(object_type: Instance) -> Optional[TypeType]:
    form_class_sym = object_type.type.get('form_class')
    if form_class_sym and isinstance(form_class_sym.type, CallableType):
        return TypeType(form_class_sym.type.ret_type)
    return None


def extract_proper_type_for_get_form(ctx: MethodContext) -> MypyType:
    object_type = ctx.type
    assert isinstance(object_type, Instance)

    form_class_type = chk_helpers.get_call_argument_type_by_name(ctx, 'form_class')
    if form_class_type is None or isinstance(form_class_type, NoneTyp):
        form_class_type = get_specified_form_class(object_type)

    if isinstance(form_class_type, TypeType) and isinstance(form_class_type.item, Instance):
        return form_class_type.item

    if isinstance(form_class_type, CallableType) and isinstance(form_class_type.ret_type, Instance):
        return form_class_type.ret_type

    return ctx.default_return_type


def extract_proper_type_for_get_form_class(ctx: MethodContext) -> MypyType:
    object_type = ctx.type
    assert isinstance(object_type, Instance)

    form_class_type = get_specified_form_class(object_type)
    if form_class_type is None:
        return ctx.default_return_type

    return form_class_type
