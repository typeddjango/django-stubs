from typing import Dict, Optional, Type, Tuple, NamedTuple

from mypy.nodes import SymbolTableNode, Var, Expression, MemberExpr
from mypy.plugin import FunctionContext
from mypy.types import Instance

MODEL_CLASS_FULLNAME = 'django.db.models.base.Model'
QUERYSET_CLASS_FULLNAME = 'django.db.models.query.QuerySet'
FOREIGN_KEY_FULLNAME = 'django.db.models.fields.related.ForeignKey'
ONETOONE_FIELD_FULLNAME = 'django.db.models.fields.related.OneToOneField'


def create_new_symtable_node(name: str, kind: int, instance: Instance) -> SymbolTableNode:
    new_var = Var(name, instance)
    new_var.info = instance.type

    return SymbolTableNode(kind, new_var,
                           plugin_generated=True)


Argument = NamedTuple('Argument', fields=[
    ('arg', Expression),
    ('arg_type', Type)
])


def get_call_signature_or_none(ctx: FunctionContext) -> Optional[Dict[str, Argument]]:
    arg_names = ctx.context.arg_names

    result: Dict[str, Argument] = {}
    positional_args_only = []
    positional_arg_types_only = []
    for arg, arg_name, arg_type in zip(ctx.args, arg_names, ctx.arg_types):
        if arg_name is None:
            positional_args_only.append(arg)
            positional_arg_types_only.append(arg_type)
            continue

        if len(arg) == 0 or len(arg_type) == 0:
            continue

        result[arg_name] = (arg[0], arg_type[0])

    callee = ctx.context.callee
    if '__init__' not in callee.node.names:
        return None

    init_type = callee.node.names['__init__'].type
    arg_names = init_type.arg_names[1:]
    for arg, arg_name, arg_type in zip(positional_args_only,
                                       arg_names[:len(positional_args_only)],
                                       positional_arg_types_only):
        result[arg_name] = (arg[0], arg_type[0])

    return result
