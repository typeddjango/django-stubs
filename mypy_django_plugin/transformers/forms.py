from __future__ import annotations

from typing import TYPE_CHECKING

from mypy_django_plugin.lib import helpers

if TYPE_CHECKING:
    from mypy.plugin import ClassDefContext


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
    else:
        meta_node.fallback_to_any = True
