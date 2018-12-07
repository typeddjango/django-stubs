import os
from typing import Callable, Optional, cast

from mypy.checker import TypeChecker
from mypy.options import Options
from mypy.plugin import Plugin, FunctionContext, ClassDefContext, AnalyzeTypeContext
from mypy.types import Type, Instance
from mypy.typevars import fill_typevars

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.plugins.fields import determine_type_of_array_field
from mypy_django_plugin.plugins.models import process_model_class
from mypy_django_plugin.plugins.related_fields import extract_to_parameter_as_get_ret_type_for_related_field, reparametrize_with
from mypy_django_plugin.plugins.settings import DjangoConfSettingsInitializerHook


base_model_classes = {helpers.MODEL_CLASS_FULLNAME}
manager_subclasses = set()


def transform_model_class(ctx: ClassDefContext) -> None:
    base_model_classes.add(ctx.cls.fullname)
    process_model_class(ctx)


def add_new_manager_subclass(ctx: ClassDefContext) -> None:
    manager_subclasses.add(ctx.cls.fullname)


def determine_proper_manager_type(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    ret = ctx.default_return_type
    if not api.tscope.classes:
        # not in class
        return ret
    outer_model_info = api.tscope.classes[0]
    if not outer_model_info.has_base(helpers.MODEL_CLASS_FULLNAME):
        return ret
    if not isinstance(ret, Instance):
        return ret

    for i, base in enumerate(ret.type.bases):
        if base.type.fullname() in {helpers.MANAGER_CLASS_FULLNAME,
                                    helpers.RELATED_MANAGER_CLASS_FULLNAME,
                                    helpers.BASE_MANAGER_CLASS_FULLNAME}:
            ret.type.bases[i] = reparametrize_with(base, [Instance(outer_model_info, [])])
            return ret
    return ret


class DjangoPlugin(Plugin):
    def __init__(self,
                 options: Options) -> None:
        super().__init__(options)
        monkeypatch.replace_apply_function_plugin_method()
        monkeypatch.make_inner_classes_with_inherit_from_any_compatible_with_each_other()

        self.django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        if self.django_settings:
            monkeypatch.load_graph_to_add_settings_file_as_a_source_seed(self.django_settings)
            monkeypatch.inject_dependencies(self.django_settings)
        else:
            monkeypatch.restore_original_load_graph()
            monkeypatch.restore_original_dependencies_handling()

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname in {helpers.FOREIGN_KEY_FULLNAME,
                        helpers.ONETOONE_FIELD_FULLNAME,
                        helpers.MANYTOMANY_FIELD_FULLNAME}:
            return extract_to_parameter_as_get_ret_type_for_related_field

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field

        if fullname in manager_subclasses:
            return determine_proper_manager_type
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in base_model_classes:
            return transform_model_class

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return DjangoConfSettingsInitializerHook(settings_module=self.django_settings)

        if fullname in helpers.MANAGER_CLASSES:
            return add_new_manager_subclass
        return None


def plugin(version):
    return DjangoPlugin
