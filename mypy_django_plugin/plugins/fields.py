from typing import Iterator, List, cast

from mypy.nodes import ClassDef, AssignmentStmt, CallExpr
from mypy.plugin import FunctionContext, ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Type, Instance

from mypy_django_plugin.plugins.related_fields import add_new_var_node_to_class


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    if 'base_field' not in ctx.arg_names:
        return ctx.default_return_type

    base_field_arg_type = ctx.arg_types[ctx.arg_names.index('base_field')][0]
    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[base_field_arg_type.type.names['__get__'].type.ret_type])


def get_assignments(klass: ClassDef) -> List[AssignmentStmt]:
    stmts = []
    for stmt in klass.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # not supported yet
            continue
        stmts.append(stmt)
    return stmts


def add_int_id_attribute_if_primary_key_true_is_not_present(ctx: ClassDefContext) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    for stmt in get_assignments(ctx.cls):
        if (isinstance(stmt.rvalue, CallExpr)
                and 'primary_key' in stmt.rvalue.arg_names
                    and api.parse_bool(stmt.rvalue.args[stmt.rvalue.arg_names.index('primary_key')])):
            break
    else:
        add_new_var_node_to_class(ctx.cls.info, 'id', api.builtin_type('builtins.int'))

