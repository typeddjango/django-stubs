from typing import List, Optional, cast

from mypy.nodes import ClassDef, Context, MypyFile, SymbolNode, SymbolTableNode, Var
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance, NoneTyp, Type, UnionType


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


def load_settings_from_module(settings_classdef: ClassDef, module: MypyFile) -> None:
    for name, sym in module.names.items():
        if name.isupper() and isinstance(sym.node, Var):
            if sym.type is not None:
                copied = make_sym_copy_of_setting(sym)
                if copied is None:
                    continue
                settings_classdef.info.names[name] = copied


class AddSettingValuesToDjangoConfObject:
    def __init__(self, settings_modules: List[str], ignore_missing_settings: bool):
        self.settings_modules = settings_modules
        self.ignore_missing_settings = ignore_missing_settings

    def __call__(self, ctx: ClassDefContext) -> None:
        api = cast(SemanticAnalyzerPass2, ctx.api)
        for module_name in self.settings_modules:
            module = api.modules[module_name]
            load_settings_from_module(ctx.cls, module=module)

        if self.ignore_missing_settings:
            ctx.cls.info.fallback_to_any = True
