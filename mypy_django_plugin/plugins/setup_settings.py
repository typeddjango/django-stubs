from typing import cast, Any

from django.conf import Settings
from mypy.nodes import MDEF, TypeInfo, SymbolTable
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance, AnyType, TypeOfAny

from mypy_django_plugin import helpers


def get_obj_type_name(value: Any) -> str:
    return type(value).__module__ + '.' + type(value).__qualname__


class DjangoConfSettingsInitializerHook(object):
    def __init__(self, settings: Settings):
        self.settings = settings

    def __call__(self, ctx: ClassDefContext) -> None:
        api = cast(SemanticAnalyzerPass2, ctx.api)
        for name, value in self.settings.__dict__.items():
            if name.isupper():
                if value is None:
                    ctx.cls.info.names[name] = helpers.create_new_symtable_node(name, MDEF,
                                                                                instance=api.builtin_type('builtins.object'))
                    continue

                type_fullname = get_obj_type_name(value)
                sym = api.lookup_fully_qualified_or_none(type_fullname)
                if sym is not None:
                    args = len(sym.node.type_vars) * [AnyType(TypeOfAny.from_omitted_generics)]
                    ctx.cls.info.names[name] = helpers.create_new_symtable_node(name, MDEF,
                                                                                instance=Instance(sym.node, args))
