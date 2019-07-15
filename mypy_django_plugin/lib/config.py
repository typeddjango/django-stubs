import os
from configparser import ConfigParser
from typing import Dict, List, Optional

import dataclasses
from dataclasses import dataclass
from pytest_mypy.utils import temp_environ


@dataclass
class Config:
    django_settings_module: Optional[str] = None
    installed_apps: List[str] = dataclasses.field(default_factory=list)

    ignore_missing_settings: bool = False
    ignore_missing_model_attributes: bool = False

    @classmethod
    def from_config_file(cls, fpath: str) -> 'Config':
        ini_config = ConfigParser()
        ini_config.read(fpath)
        if not ini_config.has_section('mypy_django_plugin'):
            raise ValueError('Invalid config file: no [mypy_django_plugin] section')

        django_settings = ini_config.get('mypy_django_plugin', 'django_settings',
                                         fallback=None)
        if django_settings:
            django_settings = django_settings.strip()

        return Config(django_settings_module=django_settings,
                      ignore_missing_settings=bool(ini_config.get('mypy_django_plugin',
                                                                  'ignore_missing_settings',
                                                                  fallback=False)),
                      ignore_missing_model_attributes=bool(ini_config.get('mypy_django_plugin',
                                                                          'ignore_missing_model_attributes',
                                                                          fallback=False)))


def extract_app_model_aliases(settings_module: str) -> Dict[str, str]:
    with temp_environ():
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
        import django
        django.setup()

    app_model_mapping: Dict[str, str] = {}

    from django.apps import apps

    for name, app_config in apps.app_configs.items():
        app_label = app_config.label
        for model_name, model_class in app_config.models.items():
            app_model_mapping[app_label + '.' + model_class.__name__] = model_class.__module__ + '.' + model_class.__name__

    return app_model_mapping
