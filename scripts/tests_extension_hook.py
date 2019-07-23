from pytest_mypy.collect import File
from pytest_mypy.item import YamlTestItem


def django_plugin_hook(test_item: YamlTestItem) -> None:
    settings = {
        'SECRET_KEY': '"1"',
    }
    additional_settings = test_item.parsed_test_data.get('additional_settings')
    if additional_settings:
        for item in additional_settings:
            name, _, val = item.partition('=')
            settings[name] = val

    installed_apps = test_item.parsed_test_data.get('installed_apps', None)
    if installed_apps is not None:
        installed_apps += ['django.contrib.contenttypes']
        installed_apps_as_str = '(' + ','.join([repr(app) for app in installed_apps]) + ',)'

        pyproject_toml_file = File(path='pyproject.toml',
                                   content='[tool.django-stubs]\ndjango_settings_module=\'mysettings\'')
        test_item.files.append(pyproject_toml_file)

        settings_contents = f'INSTALLED_APPS={installed_apps_as_str}\n'
        settings_contents += '\n'.join([f'{key}={val}' for key, val in settings.items()])

        mysettings_file = File(path='mysettings.py', content=settings_contents)
        test_item.files.append(mysettings_file)
