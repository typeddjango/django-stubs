from test.pytest_plugin import reveal_type, file, env
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestParseSettingsFromFile(BaseDjangoPluginTestCase):
    @env(DJANGO_SETTINGS_MODULE='mysettings')
    def test_case(self):
        from django.conf import settings

        reveal_type(settings.ROOT_DIR)  # E: Revealed type is 'builtins.str'
        reveal_type(settings.OBJ)  # E: Revealed type is 'django.utils.functional.LazyObject'
        reveal_type(settings.NUMBERS)  # E: Revealed type is 'builtins.list[builtins.str]'
        reveal_type(settings.DICT)  # E: Revealed type is 'builtins.dict[Any, Any]'

    @file('mysettings.py')
    def mysettings_py_file(self):
        SECRET_KEY = 112233
        ROOT_DIR = '/etc'
        NUMBERS = ['one', 'two']
        DICT = {}  # type: ignore

        from django.utils.functional import LazyObject

        OBJ = LazyObject()


class TestSettingInitializableToNone(BaseDjangoPluginTestCase):
    @env(DJANGO_SETTINGS_MODULE='mysettings')
    def test_case(self):
        from django.conf import settings

        reveal_type(settings.NONE_SETTING)  # E: Revealed type is 'builtins.object'

    @file('mysettings.py')
    def mysettings_py_file(self):
        SECRET_KEY = 112233
        NONE_SETTING: object = None
