from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext


def inject_any_as_base_for_nested_class_meta(ctx: ClassDefContext) -> None:
    if 'Meta' not in ctx.cls.info.names:
        return None
    sym = ctx.cls.info.names['Meta']
    if not isinstance(sym.node, TypeInfo):
        return None

    sym.node.fallback_to_any = True
