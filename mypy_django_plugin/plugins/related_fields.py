import typing
from typing import Optional, cast

from django.conf import Settings
from mypy.checker import TypeChecker
from mypy.nodes import SymbolTable, MDEF, AssignmentStmt
from mypy.plugin import FunctionContext, ClassDefContext
from mypy.types import Type, CallableType, Instance, AnyType, TypeOfAny

from mypy_django_plugin import helpers


def extract_related_name_value(ctx: FunctionContext) -> str:
    return ctx.context.args[ctx.arg_names.index('related_name')].value


def reparametrize_with(instance: Instance, new_typevars: typing.List[Type]):
    return Instance(instance.type, args=new_typevars)


def fill_typevars_with_any(instance: Instance) -> Type:
    return reparametrize_with(instance, [AnyType(TypeOfAny.unannotated)])


def get_valid_to_value_or_none(ctx: FunctionContext) -> Optional[Instance]:
    if 'to' not in ctx.arg_names:
        # shouldn't happen, invalid code
        ctx.api.msg.fail(f'to= parameter must be set for {ctx.context.callee.fullname}',
                         context=ctx.context)
        return None

    arg_type = ctx.arg_types[ctx.arg_names.index('to')][0]
    if not isinstance(arg_type, CallableType):
        ctx.api.msg.warn(f'to= parameter type {arg_type.__class__.__name__} is not supported',
                         context=ctx.context)
        return None

    referred_to_type = arg_type.ret_type
    for base in referred_to_type.type.bases:
        if base.type.fullname() == helpers.MODEL_CLASS_FULLNAME:
            break
    else:
        ctx.api.msg.fail(f'to= parameter value must be '
                         f'a subclass of {helpers.MODEL_CLASS_FULLNAME}',
                         context=ctx.context)
        return None

    return referred_to_type


class ForeignKeyHook(object):
    def __init__(self, settings: Settings):
        self.settings = settings

    def __call__(self, ctx: FunctionContext) -> Type:
        api = cast(TypeChecker, ctx.api)
        outer_class_info = api.tscope.classes[-1]

        referred_to_type = get_valid_to_value_or_none(ctx)
        if referred_to_type is None:
            return fill_typevars_with_any(ctx.default_return_type)

        if 'related_name' in ctx.arg_names:
            related_name = extract_related_name_value(ctx)
            queryset_type = api.named_generic_type(helpers.QUERYSET_CLASS_FULLNAME,
                                                   args=[Instance(outer_class_info, [])])
            sym = helpers.create_new_symtable_node(related_name, MDEF,
                                                   instance=queryset_type)
            referred_to_type.type.names[related_name] = sym

        return reparametrize_with(ctx.default_return_type, [referred_to_type])


class OneToOneFieldHook(object):
    def __init__(self, settings: Optional[Settings]):
        self.settings = settings

    def __call__(self, ctx: FunctionContext) -> Type:
        api = cast(TypeChecker, ctx.api)
        outer_class_info = api.tscope.classes[-1]

        referred_to_type = get_valid_to_value_or_none(ctx)
        if referred_to_type is None:
            return fill_typevars_with_any(ctx.default_return_type)

        if 'related_name' in ctx.arg_names:
            related_name = extract_related_name_value(ctx)
            sym = helpers.create_new_symtable_node(related_name, MDEF,
                                                   instance=Instance(outer_class_info, []))
            referred_to_type.type.names[related_name] = sym

        return reparametrize_with(ctx.default_return_type, [referred_to_type])


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
