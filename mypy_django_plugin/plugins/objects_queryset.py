from typing import cast

from mypy.nodes import MDEF, AssignmentStmt
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance

from mypy_django_plugin import helpers


def set_objects_queryset_to_model_class(ctx: ClassDefContext) -> None:
    if 'objects' in ctx.cls.info.names:
        return
    api = cast(SemanticAnalyzerPass2, ctx.api)

    metaclass_node = ctx.cls.info.names.get('Meta')
    if metaclass_node is not None:
        for stmt in metaclass_node.node.defn.defs.body:
            if (isinstance(stmt, AssignmentStmt) and len(stmt.lvalues) == 1
                    and stmt.lvalues[0].name == 'abstract'):
                is_abstract = api.parse_bool(stmt.rvalue)
                if is_abstract:
                    return

    typ = api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME, args=[Instance(ctx.cls.info, [])])
    new_objects_node = helpers.create_new_symtable_node('objects', MDEF, instance=typ)
    ctx.cls.info.names['objects'] = new_objects_node
