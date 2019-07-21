# noinspection PyUnresolvedReferences
from pytest_mypy.collect import (  # noqa: F401
    File, YamlTestFile, pytest_addoption,
)
from pytest_mypy.item import YamlTestItem


class DjangoYamlTestFile(YamlTestFile):
    def get_test_class(self):
        return NewSemanalDjangoTestItem


def pytest_collect_file(path, parent):
    if path.ext in {'.yaml', '.yml'} and path.basename.startswith(('test-', 'test_')):
        return DjangoYamlTestFile(path, parent=parent, config=parent.config)


class NewSemanalDjangoTestItem(YamlTestItem):
    def custom_init(self):
        settings = {
            'SECRET_KEY': '"1"',
        }
        additional_settings = self.parsed_test_data.get('additional_settings')
        if additional_settings:
            for item in additional_settings:
                name, _, val = item.partition('=')
                settings[name] = val

        installed_apps = self.parsed_test_data.get('installed_apps', None)
        if installed_apps is not None:
            installed_apps += ['django.contrib.contenttypes']
            installed_apps_as_str = '(' + ','.join([repr(app) for app in installed_apps]) + ',)'

            pyproject_toml_file = File(path='pyproject.toml',
                                       content='[tool.django-stubs]\ndjango_settings_module=\'mysettings\'')
            self.files.append(pyproject_toml_file)

            settings_contents = f'INSTALLED_APPS={installed_apps_as_str}\n'
            settings_contents += '\n'.join([f'{key}={val}' for key, val in settings.items()])

            mysettings_file = File(path='mysettings.py', content=settings_contents)
            self.files.append(mysettings_file)
