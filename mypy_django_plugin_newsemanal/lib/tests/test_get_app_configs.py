from mypy.options import Options

from mypy_django_plugin.lib.config import extract_app_model_aliases
from mypy_django_plugin.main import DjangoPlugin


def test_parse_django_settings():
    app_model_mapping = extract_app_model_aliases('mypy_django_plugin.lib.tests.sample_django_project.root.settings')
    assert app_model_mapping['myapp.MyModel'] == 'mypy_django_plugin.lib.tests.sample_django_project.myapp.models.MyModel'


def test_instantiate_plugin_with_config():
    plugin = DjangoPlugin(Options())

