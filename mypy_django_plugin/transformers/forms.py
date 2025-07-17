from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext

from mypy_django_plugin.lib import fullnames, helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
    else:
        meta_node.fallback_to_any = True


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        bases = helpers.get_django_metadata_bases(sym.node, "baseform_bases")
        bases[ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)
