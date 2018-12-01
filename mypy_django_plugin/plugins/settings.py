from typing import cast, List

from mypy.nodes import Var, Context, SymbolNode, SymbolTableNode
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance, UnionType, NoneTyp, Type

from mypy_django_plugin import helpers


def get_error_context(node: SymbolNode) -> Context:
    context = Context()
    context.set_line(node)
    return context


def filter_out_nones(typ: UnionType) -> List[Type]:
    return [item for item in typ.items if not isinstance(item, NoneTyp)]


def copy_sym_of_instance(sym: SymbolTableNode) -> SymbolTableNode:
    copied = sym.copy()
    copied.node.info = sym.type.type
    return copied


def add_settings_to_django_conf_object(ctx: ClassDefContext,
                                       settings_module: str) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    if settings_module not in api.modules:
        return None

    settings_file = api.modules[settings_module]
    for name, sym in settings_file.names.items():
        if name.isupper() and isinstance(sym.node, Var):
            if isinstance(sym.type, Instance):
                copied = sym.copy()
                copied.node.info = sym.type.type
                ctx.cls.info.names[name] = copied

            elif isinstance(sym.type, UnionType):
                instances = filter_out_nones(sym.type)
                if len(instances) > 1:
                    # plain unions not supported yet
                    continue
                typ = instances[0]
                if isinstance(typ, Instance):
                    copied = sym.copy()
                    copied.node.info = typ.type
                    ctx.cls.info.names[name] = copied


class DjangoConfSettingsInitializerHook(object):
    def __init__(self, settings_module: str):
        self.settings_module = settings_module

    def __call__(self, ctx: ClassDefContext) -> None:
        if not self.settings_module:
            return

        add_settings_to_django_conf_object(ctx, self.settings_module)
