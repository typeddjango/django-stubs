from typing import Optional, Any, cast

from mypy.nodes import Var, Context, GDEF
from mypy.options import Options
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance


def add_settings_to_django_conf_object(ctx: ClassDefContext,
                                       settings_module: str) -> Optional[Any]:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    if settings_module not in api.modules:
        return None

    settings_file = api.modules[settings_module]
    for name, sym in settings_file.names.items():
        if name.isupper():
            if not isinstance(sym.node, Var) or not isinstance(sym.type, Instance):
                error_context = Context()
                error_context.set_line(sym.node)
                api.msg.fail("Need type annotation for '{}'".format(sym.node.name()),
                             context=error_context,
                             file=settings_file.path,
                             origin=Context())
                continue

            sym_copy = sym.copy()
            sym_copy.node.info = sym_copy.type.type
            sym_copy.kind = GDEF
            ctx.cls.info.names[name] = sym_copy


class DjangoConfSettingsInitializerHook(object):
    def __init__(self, settings_module: str):
        self.settings_module = settings_module

    def __call__(self, ctx: ClassDefContext) -> None:
        if not self.settings_module:
            return

        add_settings_to_django_conf_object(ctx, self.settings_module)
