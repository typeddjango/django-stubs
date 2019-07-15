import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, Type

from django.db.models.base import Model
from django.utils.functional import cached_property
from pytest_mypy.utils import temp_environ

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.conf import LazySettings


@dataclass
class DjangoPluginConfig:
    ignore_missing_settings: bool = False
    ignore_missing_model_attributes: bool = False


def initialize_django(settings_module: str) -> Tuple['Apps', 'LazySettings']:
    with temp_environ():
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

        def noop_class_getitem(cls, key):
            return cls

        from django.db import models

        models.QuerySet.__class_getitem__ = classmethod(noop_class_getitem)
        models.Manager.__class_getitem__ = classmethod(noop_class_getitem)

        from django.conf import settings
        from django.apps import apps

        apps.get_models.cache_clear()
        apps.get_swappable_settings_name.cache_clear()

        apps.populate(settings.INSTALLED_APPS)

    assert apps.apps_ready
    assert settings.configured

    return apps, settings


class DjangoContext:
    def __init__(self, plugin_toml_config: Optional[Dict[str, Any]]) -> None:
        self.config = DjangoPluginConfig()

        django_settings_module = None
        if plugin_toml_config:
            self.config.ignore_missing_settings = plugin_toml_config.get('ignore_missing_settings', False)
            self.config.ignore_missing_model_attributes = plugin_toml_config.get('ignore_missing_model_attributes', False)
            django_settings_module = plugin_toml_config.get('django_settings_module', None)

        self.apps_registry: Optional[Dict[str, str]] = None
        self.settings: LazySettings = None
        if django_settings_module:
            apps, settings = initialize_django(django_settings_module)
            self.apps_registry = apps
            self.settings = settings

    @cached_property
    def model_modules(self) -> Dict[str, List[Type[Model]]]:
        """ All modules that contain Django models. """
        if self.apps_registry is None:
            return {}

        modules: Dict[str, List[Type[Model]]] = defaultdict(list)
        for model_cls in self.apps_registry.get_models():
            modules[model_cls.__module__].append(model_cls)
        return modules

    def get_model_class_by_fullname(self, fullname: str) -> Optional[Type[Model]]:
        # Returns None if Model is abstract
        module, _, model_cls_name = fullname.rpartition('.')
        for model_cls in self.model_modules.get(module, []):
            if model_cls.__name__ == model_cls_name:
                return model_cls
