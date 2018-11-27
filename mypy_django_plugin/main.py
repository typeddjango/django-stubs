import os
from typing import Callable, Optional

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
    def __call__(self, ctx: ClassDefContext) -> None:
        base_model_classes.add(ctx.cls.fullname)

        set_fieldname_attrs_for_related_fields(ctx)
        set_objects_queryset_to_model_class(ctx)


class DjangoPlugin(Plugin):
    def __init__(self,
                 options: Options) -> None:
        super().__init__(options)
        monkeypatch.replace_apply_function_plugin_method()

        self.django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        if self.django_settings:
            monkeypatch.load_graph_to_add_settings_file_as_a_source_seed(self.django_settings)
            monkeypatch.inject_dependencies(self.django_settings)
        else:
            monkeypatch.restore_original_load_graph()
            monkeypatch.restore_original_dependencies_handling()

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == helpers.FOREIGN_KEY_FULLNAME:
            return ForeignKeyHook(settings=self.django_settings)

        if fullname == helpers.ONETOONE_FIELD_FULLNAME:
            return OneToOneFieldHook(settings=self.django_settings)

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in base_model_classes:
            return TransformModelClassHook()

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return DjangoConfSettingsInitializerHook(settings_module=self.django_settings)

        return None


def plugin(version):
    return DjangoPlugin
