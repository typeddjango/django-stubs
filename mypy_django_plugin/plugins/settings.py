from typing import cast, List, Optional

from mypy.nodes import Var, Context, SymbolNode, SymbolTableNode
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance, UnionType, NoneTyp, Type


def get_error_context(node: SymbolNode) -> Context:
    context = Context()
    context.set_line(node)
    return context


def filter_out_nones(typ: UnionType) -> List[Type]:
    return [item for item in typ.items if not isinstance(item, NoneTyp)]


def make_sym_copy_of_setting(sym: SymbolTableNode) -> Optional[SymbolTableNode]:
    if isinstance(sym.type, Instance):
        copied = sym.copy()
        copied.node.info = sym.type.type
        return copied
    elif isinstance(sym.type, UnionType):
        instances = filter_out_nones(sym.type)
        if len(instances) > 1:
            # plain unions not supported yet
            return None
        typ = instances[0]
        if isinstance(typ, Instance):
            copied = sym.copy()
            copied.node.info = typ.type
            return copied
        return None
    else:
        return None


def add_settings_to_django_conf_object(ctx: ClassDefContext,
                                       settings_module: str) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    if settings_module not in api.modules:
        return None

    settings_file = api.modules[settings_module]
    for name, sym in settings_file.names.items():
        if name.isupper() and isinstance(sym.node, Var):
            if sym.type is not None:
                copied = make_sym_copy_of_setting(sym)
                if copied is None:
                    continue
                ctx.cls.info.names[name] = copied
            # else:
                # TODO: figure out suggestion to add type annotation
                # context = Context()
                # module, node_name = sym.node.fullname().rsplit('.', 1)
                # module_file = api.modules.get(module)
                # if module_file is None:
                #     return None
                # context.set_line(sym.node)
                # api.msg.report(f"Need type annotation for '{sym.node.name()}'", context,
                #                severity='error', file=module_file.path)
    ctx.cls.info.fallback_to_any = True


class DjangoConfSettingsInitializerHook(object):
    def __init__(self, settings_module: Optional[str]):
        self.settings_module = settings_module

    def __call__(self, ctx: ClassDefContext) -> None:
        if not self.settings_module:
            return

        add_settings_to_django_conf_object(ctx, self.settings_module)
