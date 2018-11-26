from test.pytest_plugin import MypyTypecheckTestCase


class BaseDjangoPluginTestCase(MypyTypecheckTestCase):
    def ini_file(self):
        return """
[mypy]
plugins = mypy_django_plugin.main
        """
