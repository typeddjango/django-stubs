from typing import Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo, SymbolTable, MDEF, AssignmentStmt, MemberExpr
from mypy.plugin import FunctionContext, ClassDefContext
from mypy.types import Type, CallableType, Instance, AnyType

from mypy_django_plugin import helpers


def extract_to_value_type(ctx: FunctionContext) -> Optional[Instance]:
    signature = helpers.get_call_signature_or_none(ctx)
    if signature is None or 'to' not in signature:
        return None

    arg, arg_type = signature['to']
    if not isinstance(arg_type, CallableType):
        return None

    return arg_type.ret_type


def extract_related_name_value(ctx: FunctionContext) -> str:
    return ctx.context.args[ctx.context.arg_names.index('related_name')].value


def add_new_class_member(klass_typeinfo: TypeInfo, name: str, new_member_instance: Instance) -> None:
    klass_typeinfo.names[name] = helpers.create_new_symtable_node(name,
                                                                  kind=MDEF,
                                                                  instance=new_member_instance)


def set_related_name_manager_for_foreign_key(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    outer_class_info = api.tscope.classes[-1]

    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    referred_to = extract_to_value_type(ctx)
    if not referred_to:
        return ctx.default_return_type

    related_name = extract_related_name_value(ctx)
    queryset_type = api.named_generic_type(helpers.QUERYSET_CLASS_FULLNAME,
                                           args=[Instance(outer_class_info, [])])
    if isinstance(referred_to, AnyType):
        # referred_to defined as string, which is unsupported for now
        return ctx.default_return_type

    add_new_class_member(referred_to.type,
                         related_name, queryset_type)
    return ctx.default_return_type


def set_related_name_instance_for_onetoonefield(ctx: FunctionContext) -> Type:
    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    referred_to = extract_to_value_type(ctx)
    if referred_to is None:
        return ctx.default_return_type

    related_name = extract_related_name_value(ctx)
    outer_class_info = ctx.api.tscope.classes[-1]

    api = cast(TypeChecker, ctx.api)
    add_new_class_member(referred_to.type, related_name,
                         new_member_instance=api.named_type(outer_class_info.fullname()))
    return ctx.default_return_type


def set_fieldname_attrs_for_related_fields(ctx: ClassDefContext) -> None:
    api = ctx.api

    new_symtable_nodes = SymbolTable()
    for (name, symtable_node), stmt in zip(ctx.cls.info.names.items(), ctx.cls.defs.body):
        if not isinstance(stmt, AssignmentStmt):
            continue
        if not hasattr(stmt.rvalue, 'callee'):
            continue

        rvalue_callee = stmt.rvalue.callee
        if rvalue_callee.fullname in {helpers.FOREIGN_KEY_FULLNAME,
                                      helpers.ONETOONE_FIELD_FULLNAME}:
            name += '_id'
            new_node = helpers.create_new_symtable_node(name,
                                                        kind=MDEF,
                                                        instance=api.named_type('__builtins__.int'))
            new_symtable_nodes[name] = new_node

    for name, node in new_symtable_nodes.items():
        ctx.cls.info.names[name] = node
