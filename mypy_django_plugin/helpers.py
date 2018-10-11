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
        return mypy_api.lookup_qualified('typing.Any')
        # return mypy_api.modules['typing'].names['Any']


def get_app_model(model_name: str) -> str:
    import os
    os.environ.setdefault('SITE_URL', 'https://localhost')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server._config.settings.local')

    import django
    django.setup()

    from django.apps import apps

    try:
        app_name, model_name = model_name.rsplit('.', maxsplit=1)
        model = apps.get_model(app_name, model_name)
        return model.__module__ + '.' + model_name
    except ValueError:
        return model_name
