from mypy.checker import TypeChecker
from mypy.nodes import SymbolTableNode, Var


def is_class_variable(symbol_table_node: SymbolTableNode) -> bool:
    # MDEF: class member definition
    is_class_variable = symbol_table_node.kind == 2 and type(symbol_table_node.node) == Var
    if not is_class_variable:
        return False

    return True


def lookup_django_model(mypy_api: TypeChecker, fullname: str) -> SymbolTableNode:
    module, _, model_name = fullname.rpartition('.')
    try:
        return mypy_api.modules[module].names[model_name]
    except KeyError:
        return mypy_api.modules['django.db.models'].names['Model']