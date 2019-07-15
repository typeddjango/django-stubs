from typing import cast

from mypy.checker import TypeChecker
from mypy.nodes import Argument, Var, ARG_NAMED
from mypy.plugin import FunctionContext
from mypy.types import Type as MypyType, Instance

from mypy_django_plugin_newsemanal.context import DjangoContext
from mypy_django_plugin_newsemanal.lib import helpers


def redefine_and_typecheck_model_init(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    assert isinstance(ctx.default_return_type, Instance)

    api = cast(TypeChecker, ctx.api)

    model_info = ctx.default_return_type.type
    model_cls = django_context.get_model_class_by_fullname(model_info.fullname())

    # expected_types = {}
    # for field in model_cls._meta.get_fields():
    #     field_fullname = helpers.get_class_fullname(field.__class__)
    #     field_info = api.lookup_typeinfo(field_fullname)
    #     field_set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
    #                                                          is_nullable=False)
    # field_kwarg = Argument(variable=Var(field.attname, field_set_type),
    #                        type_annotation=field_set_type,
    #                        initializer=None,
    #                        kind=ARG_NAMED)
    # expected_types[field.attname] = field_set_type
    # for field_name, field in model_cls._meta.fields_map.items():
    #     print()

    # print()
    return ctx.default_return_type
