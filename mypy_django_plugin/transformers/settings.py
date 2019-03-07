from typing import Iterable, List, Optional, cast

from mypy.nodes import (
    ClassDef, Context, ImportAll, MypyFile, SymbolNode, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import AnyType, Instance, NoneTyp, Type, TypeOfAny, UnionType
from mypy.util import correct_relative_import


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


def get_settings_metadata(lazy_settings_info: TypeInfo):
    return lazy_settings_info.metadata.setdefault('django', {}).setdefault('settings', {})


def load_settings_from_names(settings_classdef: ClassDef,
                             modules: Iterable[MypyFile],
                             api: SemanticAnalyzerPass2) -> None:
    settings_metadata = get_settings_metadata(settings_classdef.info)

    for module in modules:
        for name, sym in module.names.items():
            if name.isupper() and isinstance(sym.node, Var):
                if sym.type is not None:
                    copied = make_sym_copy_of_setting(sym)
                    if copied is None:
                        continue
                    settings_classdef.info.names[name] = copied
                else:
                    var = Var(name, AnyType(TypeOfAny.unannotated))
                    var.info = api.named_type('__builtins__.object').type  # outer class type
                    settings_classdef.info.names[name] = SymbolTableNode(sym.kind, var, plugin_generated=True)

                settings_metadata[name] = module.fullname()


def get_import_star_modules(api: SemanticAnalyzerPass2, module: MypyFile) -> List[str]:
    import_star_modules = []
    for module_import in module.imports:
        # relative import * are not resolved by mypy
        if isinstance(module_import, ImportAll) and module_import.relative:
            absolute_import_path, correct = correct_relative_import(module.fullname(), module_import.relative,
                                                                    module_import.id, is_cur_package_init_file=False)
            if not correct:
                return []
            for path in [absolute_import_path] + get_import_star_modules(api,
                                                                         module=api.modules.get(absolute_import_path)):
                if path not in import_star_modules:
                    import_star_modules.append(path)
    return import_star_modules


class AddSettingValuesToDjangoConfObject:
    def __init__(self, settings_modules: List[str], ignore_missing_settings: bool):
        self.settings_modules = settings_modules
        self.ignore_missing_settings = ignore_missing_settings

    def __call__(self, ctx: ClassDefContext) -> None:
        api = cast(SemanticAnalyzerPass2, ctx.api)
        for module_name in self.settings_modules:
            module = api.modules[module_name]
            star_deps = [api.modules[star_dep]
                         for star_dep in reversed(get_import_star_modules(api, module))]
            load_settings_from_names(ctx.cls, modules=star_deps + [module], api=api)

        if self.ignore_missing_settings:
            ctx.cls.info.fallback_to_any = True
