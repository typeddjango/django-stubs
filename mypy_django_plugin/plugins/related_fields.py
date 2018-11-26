import typing
from typing import Optional, cast, Tuple, Any

from django.apps.registry import Apps
from django.conf import Settings
from django.db import models
from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo, SymbolTable, MDEF, AssignmentStmt, StrExpr
from mypy.plugin import FunctionContext, ClassDefContext
from mypy.types import Type, CallableType, Instance, AnyType

from mypy_django_plugin import helpers


def get_instance_type_for_class(klass: typing.Type[models.Model],
                                api: TypeChecker) -> Optional[Instance]:
    model_qualname = helpers.get_obj_type_name(klass)
    module_name, _, class_name = model_qualname.rpartition('.')
    module = api.modules.get(module_name)
    if not module or class_name not in module.names:
        return

    sym = module.names[class_name]
    return Instance(sym.node, [])


def extract_to_value_type(ctx: FunctionContext,
                          apps: Optional[Apps]) -> Tuple[Optional[Instance], bool]:
    api = cast(TypeChecker, ctx.api)

    if 'to' not in ctx.arg_names:
        return None, False
    arg = ctx.args[ctx.arg_names.index('to')][0]
    arg_type = ctx.arg_types[ctx.arg_names.index('to')][0]

    if isinstance(arg_type, CallableType):
        return arg_type.ret_type, False

    if apps:
        if isinstance(arg, StrExpr):
            arg_value = arg.value
            if '.' not in arg_value:
                return None, False

            app_label, modelname = arg_value.lower().split('.')
            try:
                model_cls = apps.get_model(app_label, modelname)
            except LookupError:
                # no model class found
                return None, False
            try:
                instance = get_instance_type_for_class(model_cls, api=api)
                if not instance:
                    return None, False
                return instance, True

            except AssertionError:
                pass

    return None, False


def extract_related_name_value(ctx: FunctionContext) -> str:
    return ctx.context.args[ctx.context.arg_names.index('related_name')].value


def add_new_class_member(klass_typeinfo: TypeInfo, name: str, new_member_instance: Instance) -> None:
    klass_typeinfo.names[name] = helpers.create_new_symtable_node(name,
                                                                  kind=MDEF,
                                                                  instance=new_member_instance)


class ForeignKeyHook(object):
    def __init__(self, settings: Settings, apps: Apps):
        self.settings = settings
        self.apps = apps

    def __call__(self, ctx: FunctionContext) -> Type:
        api = cast(TypeChecker, ctx.api)
        outer_class_info = api.tscope.classes[-1]

        referred_to, is_string_based = extract_to_value_type(ctx, apps=self.apps)
        if not referred_to:
            return ctx.default_return_type

        if 'related_name' in ctx.context.arg_names:
            related_name = extract_related_name_value(ctx)
            queryset_type = api.named_generic_type(helpers.QUERYSET_CLASS_FULLNAME,
                                                   args=[Instance(outer_class_info, [])])
            if isinstance(referred_to, AnyType):
                return ctx.default_return_type

            add_new_class_member(referred_to.type,
                                 related_name, queryset_type)
        if is_string_based:
            return referred_to

        return ctx.default_return_type


class OneToOneFieldHook(object):
    def __init__(self, settings: Optional[Settings], apps: Optional[Apps]):
        self.settings = settings
        self.apps = apps

    def __call__(self, ctx: FunctionContext) -> Type:
        if 'related_name' not in ctx.context.arg_names:
            return ctx.default_return_type

        referred_to, is_string_based = extract_to_value_type(ctx, apps=self.apps)
        if referred_to is None:
            return ctx.default_return_type

        if 'related_name' in ctx.context.arg_names:
            related_name = extract_related_name_value(ctx)
            outer_class_info = ctx.api.tscope.classes[-1]
            add_new_class_member(referred_to.type, related_name,
                                 new_member_instance=Instance(outer_class_info, []))

        if is_string_based:
            return referred_to

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
