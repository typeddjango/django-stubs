import os
from typing import Callable, Optional, cast, Dict

from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo
from mypy.options import Options
from mypy.plugin import Plugin, FunctionContext, ClassDefContext, MethodContext
from mypy.types import Type, Instance

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.plugins.fields import determine_type_of_array_field
from mypy_django_plugin.plugins.migrations import determine_model_cls_from_string_for_migrations
from mypy_django_plugin.plugins.models import process_model_class
from mypy_django_plugin.plugins.related_fields import extract_to_parameter_as_get_ret_type_for_related_field, reparametrize_with
from mypy_django_plugin.plugins.settings import DjangoConfSettingsInitializerHook


def transform_model_class(ctx: ClassDefContext) -> None:
    try:
        sym = ctx.api.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
    except KeyError:
        # models.Model is not loaded, skip metadata model write
        pass
    else:
        if sym is not None and isinstance(sym.node, TypeInfo):
            sym.node.metadata['django']['model_bases'][ctx.cls.fullname] = 1
    process_model_class(ctx)


def transform_manager_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.MANAGER_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['manager_bases'][ctx.cls.fullname] = 1


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
        monkeypatch.make_inner_classes_with_inherit_from_any_compatible_with_each_other()

        self.django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        if self.django_settings:
            monkeypatch.load_graph_to_add_settings_file_as_a_source_seed(self.django_settings)
            monkeypatch.inject_dependencies(self.django_settings)
        else:
            monkeypatch.restore_original_load_graph()
            monkeypatch.restore_original_dependencies_handling()

    def get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            if 'django' not in model_sym.node.metadata:
                model_sym.node.metadata['django'] = {
                    'model_bases': {helpers.MODEL_CLASS_FULLNAME: 1}
                }
            return model_sym.node.metadata['django']['model_bases']
        else:
            return {}

    def get_current_manager_bases(self) -> Dict[str, int]:
        manager_sym = self.lookup_fully_qualified(helpers.MANAGER_CLASS_FULLNAME)
        if manager_sym is not None and isinstance(manager_sym.node, TypeInfo):
            if 'django' not in manager_sym.node.metadata:
                manager_sym.node.metadata['django'] = {
                    'manager_bases': {helpers.MANAGER_CLASS_FULLNAME: 1}
                }
            return manager_sym.node.metadata['django']['manager_bases']
        else:
            return {}

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname in {helpers.FOREIGN_KEY_FULLNAME,
                        helpers.ONETOONE_FIELD_FULLNAME,
                        helpers.MANYTOMANY_FIELD_FULLNAME}:
            return extract_to_parameter_as_get_ret_type_for_related_field

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field

        manager_bases = self.get_current_manager_bases()
        if fullname in manager_bases:
            return determine_proper_manager_type

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        if fullname in {'django.apps.registry.Apps.get_model',
                        'django.db.migrations.state.StateApps.get_model'}:
            return determine_model_cls_from_string_for_migrations
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self.get_current_model_bases():
            return transform_model_class

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return DjangoConfSettingsInitializerHook(settings_module=self.django_settings)

        if fullname in self.get_current_manager_bases():
            return transform_manager_class

        return None


def plugin(version):
    return DjangoPlugin
