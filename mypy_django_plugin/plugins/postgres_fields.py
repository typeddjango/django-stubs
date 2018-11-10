from typing import Optional, Callable

from mypy.plugin import Plugin, FunctionContext
from mypy.types import Type


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    assert 'base_field' in ctx.context.arg_names
    base_field_arg_index = ctx.context.arg_names.index('base_field')
    base_field_arg_type = ctx.arg_types[base_field_arg_index][0]

    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[base_field_arg_type.type.names['__get__'].type.ret_type])


class PostgresFieldsPlugin(Plugin):
    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field
        return None


def plugin(version):
    return PostgresFieldsPlugin
