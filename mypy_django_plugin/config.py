from configparser import ConfigParser
from typing import Optional

from dataclasses import dataclass


@dataclass
class Config:
    django_settings_module: Optional[str] = None
    ignore_missing_settings: bool = False

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
                      ignore_missing_settings=bool(ini_config.get('mypy_django_plugin', 'ignore_missing_settings',
                                                                  fallback=False)))
