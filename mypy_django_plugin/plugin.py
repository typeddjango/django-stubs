import importlib
import inspect
from typing import Optional, Callable

from mypy.mypyc_hacks import TypeOfAny
from mypy.nodes import PassStmt, CallExpr, SymbolTableNode, MDEF, Var, ClassDef, Decorator, AssignmentStmt, StrExpr
from mypy.plugin import Plugin, ClassDefContext, AttributeContext
from mypy.types import AnyType, Type, Instance, CallableType

from mypy_django_plugin.constants import REFERENCING_DB_FIELDS, DB_FIELDS_TO_TYPES
from mypy_django_plugin.helpers import lookup_django_model
from mypy_django_plugin.model_classes import DjangoModelsRegistry, ModelInfo


model_registry = DjangoModelsRegistry()


def get_db_field_arguments(rvalue: CallExpr) -> inspect.BoundArguments:
    modulename, _, classname = rvalue.callee.fullname.rpartition('.')
    klass = getattr(importlib.import_module(modulename), classname)
    bound_signature = inspect.signature(klass).bind(*rvalue.args)

    return bound_signature


def process_meta_innerclass(class_def: ClassDef):
    pass


def get_app_model(model_name: str) -> str:
    import os
    os.environ.setdefault('SITE_URL', 'https://localhost')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server._config.settings.local')

    import django
    django.setup()

    from django.apps import apps

    try:
        app_name, model_name = model_name.rsplit('.', maxsplit=1)
        model = apps.get_model(app_name, model_name)
        return model.__module__ + '.' + model_name
    except ValueError:
        return model_name


def base_class_callback(model_def_context: ClassDefContext) -> None:
    # add new possible base models
    for base_type_expr in model_def_context.cls.base_type_exprs:
        if base_type_expr.fullname in model_registry:
            model_registry.base_models[model_def_context.cls.fullname] = ModelInfo()

    for definition in model_def_context.cls.defs.body:
        if isinstance(definition, PassStmt):
            continue

        if isinstance(definition, ClassDef):
            if definition.name == 'Meta':
                process_meta_innerclass(definition)
                continue

        if isinstance(definition, AssignmentStmt):
            rvalue = definition.rvalue
            if hasattr(rvalue, 'callee') and rvalue.callee.fullname in REFERENCING_DB_FIELDS:
                modulename, _, classname = rvalue.callee.fullname.rpartition('.')
                klass = getattr(importlib.import_module(modulename), classname)
                bound_signature = inspect.signature(klass).bind(*rvalue.args)

                to_arg_value = bound_signature.arguments['to']
                if isinstance(to_arg_value, StrExpr):
                    model_fullname = get_app_model(to_arg_value.value)
                else:
                    model_fullname = bound_signature.arguments['to'].fullname

                referred_model = model_fullname
                rvalue.callee.node.metadata['base'] = referred_model

            # if 'related_name' in rvalue.arg_names:
            #     related_name = rvalue.args[rvalue.arg_names.index('related_name')].value
            #
            #     for name, context_global in model_def_context.api.globals.items():
            #         context_global: SymbolTableNode = context_global
            #         if context_global.fullname == referred_model:
            #             list_of_any = Instance(model_def_context.api.lookup_fully_qualified('typing.List').node,
            #                                                      [AnyType(TypeOfAny.from_omitted_generics)])
            #             related_members_node = Var(related_name, list_of_any)
            #             context_global.node.names[related_name] = SymbolTableNode(MDEF, related_members_node)

                # model_registry.base_models[referred_model].related_managers[related_name] = model_def_context.cls.fullname



def related_manager_inference_callback(attr_context: AttributeContext) -> Type:
    mypy_api = attr_context.api

    default_attr_type = attr_context.default_attr_type
    if not isinstance(default_attr_type, Instance):
        return default_attr_type

    attr_type_fullname = default_attr_type.type.fullname()

    if attr_type_fullname in DB_FIELDS_TO_TYPES:
        return mypy_api.named_type(DB_FIELDS_TO_TYPES[attr_type_fullname])

    if 'base' in default_attr_type.type.metadata:
        base_class = default_attr_type.type.metadata['base']

        node = lookup_django_model(mypy_api, base_class).node
        return Instance(node, [])
        # mypy_api.lookup_qualified(base_class)
        # app = base_class.split('.')[0]
        # name = base_class.split('.')[-1]
        # app_model = get_app_model(app + '.' + name)

        # return mypy_api.named_type(name)

    return AnyType(TypeOfAny.unannotated)


#
# def type_analyze_callback(context: AnalyzeTypeContext) -> Type:
#     return context.type


class RelatedManagersDjangoPlugin(Plugin):
    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        # every time new class is created, this method is called with first base class in MRO
        if fullname in model_registry:
            return base_class_callback

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        return related_manager_inference_callback


def plugin(version):
    return RelatedManagersDjangoPlugin
