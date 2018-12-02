import typing
from typing import Dict, Optional

from mypy.nodes import StrExpr, MypyFile, TypeInfo, ImportedName, SymbolNode

MODEL_CLASS_FULLNAME = 'django.db.models.base.Model'
QUERYSET_CLASS_FULLNAME = 'django.db.models.query.QuerySet'
FOREIGN_KEY_FULLNAME = 'django.db.models.fields.related.ForeignKey'
ONETOONE_FIELD_FULLNAME = 'django.db.models.fields.related.OneToOneField'
DUMMY_SETTINGS_BASE_CLASS = 'django.conf._DjangoConfLazyObject'


def get_models_file(app_name: str, all_modules: typing.Dict[str, MypyFile]) -> Optional[MypyFile]:
    models_module = '.'.join([app_name, 'models'])
    return all_modules.get(models_module)


def get_model_fullname_from_string(expr: StrExpr,
                                   all_modules: Dict[str, MypyFile]) -> Optional[str]:
    app_name, model_name = expr.value.split('.')

    models_file = get_models_file(app_name, all_modules)
    if models_file is None:
        # not imported so far, not supported
        return None
    sym = models_file.names.get(model_name)
    if not sym:
        return None

    if isinstance(sym.node, TypeInfo):
        return sym.node.fullname()
    elif isinstance(sym.node, ImportedName):
        return sym.node.target_fullname
    else:
        return None


def lookup_fully_qualified_generic(name: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolNode]:
    if '.' not in name:
        return None
    module, cls_name = name.rsplit('.', 1)

    module_file = all_modules.get(module)
    if module_file is None:
        return None
    sym = module_file.names.get(cls_name)
    if sym is None:
        return None
    return sym.node
