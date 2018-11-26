import os
from typing import Callable, Optional, List

from django.apps.registry import Apps
from django.conf import Settings
from mypy import build
from mypy.build import BuildManager
from mypy.options import Options
from mypy.plugin import Plugin, FunctionContext, ClassDefContext
from mypy.types import Type

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.plugins.objects_queryset import set_objects_queryset_to_model_class
from mypy_django_plugin.plugins.postgres_fields import determine_type_of_array_field
from mypy_django_plugin.plugins.related_fields import OneToOneFieldHook, \
    ForeignKeyHook, set_fieldname_attrs_for_related_fields
from mypy_django_plugin.plugins.setup_settings import DjangoConfSettingsInitializerHook


base_model_classes = {helpers.MODEL_CLASS_FULLNAME}


class TransformModelClassHook(object):
    def __init__(self, settings: Settings, apps: Apps):
        self.settings = settings
        self.apps = apps

    def __call__(self, ctx: ClassDefContext) -> None:
        base_model_classes.add(ctx.cls.fullname)

        set_fieldname_attrs_for_related_fields(ctx)
        set_objects_queryset_to_model_class(ctx)


def always_return_none(manager: BuildManager):
    return None


build.read_plugins_snapshot = always_return_none


class DjangoPlugin(Plugin):
    def __init__(self,
                 options: Options) -> None:
        super().__init__(options)
        self.django_settings = None
        self.apps = None

        monkeypatch.replace_apply_function_plugin_method()

        django_settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        if django_settings_module:
            self.django_settings = Settings(django_settings_module)
            # import django
            # django.setup()
            #
            # from django.apps import apps
            # self.apps = apps
            #
            # models_modules = []
            # for app_config in self.apps.app_configs.values():
            #     models_modules.append(app_config.module.__name__ + '.' + 'models')
            #
            # monkeypatch.state_compute_dependencies_to_parse_installed_apps_setting_in_settings_module(django_settings_module,
            #                                                                                           models_modules)
            monkeypatch.load_graph_to_add_settings_file_as_a_source_seed(django_settings_module)

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == helpers.FOREIGN_KEY_FULLNAME:
            return ForeignKeyHook(settings=self.django_settings,
                                  apps=self.apps)

        if fullname == helpers.ONETOONE_FIELD_FULLNAME:
            return OneToOneFieldHook(settings=self.django_settings,
                                     apps=self.apps)

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in base_model_classes:
            return TransformModelClassHook(self.django_settings, self.apps)

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return DjangoConfSettingsInitializerHook(settings=self.django_settings)

        return None


def plugin(version):
    return DjangoPlugin
