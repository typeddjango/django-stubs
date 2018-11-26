from typing import cast

from mypy.nodes import MDEF, AssignmentStmt
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance

from mypy_django_plugin import helpers


def set_objects_queryset_to_model_class(ctx: ClassDefContext) -> None:
    # search over mro
    objects_sym = ctx.cls.info.get('objects')
    if objects_sym is not None:
        return None

    # only direct Meta class
    metaclass_sym = ctx.cls.info.names.get('Meta')
    # skip if abstract
    if metaclass_sym is not None:
        for stmt in metaclass_sym.node.defn.defs.body:
            if (isinstance(stmt, AssignmentStmt) and len(stmt.lvalues) == 1
                    and stmt.lvalues[0].name == 'abstract'):
                is_abstract = ctx.api.parse_bool(stmt.rvalue)
                if is_abstract:
                    return None

    api = cast(SemanticAnalyzerPass2, ctx.api)
    typ = api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME,
                                 args=[Instance(ctx.cls.info, [])])
    if not typ:
        return None

    ctx.cls.info.names['objects'] = helpers.create_new_symtable_node('objects',
                                                                     kind=MDEF,
                                                                     instance=typ)
