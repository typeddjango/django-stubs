import os
from typing import Callable, Dict, Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo
from mypy.options import Options
from mypy.plugin import ClassDefContext, FunctionContext, MethodContext, Plugin
from mypy.types import Instance, Type, TypeType

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.config import Config
from mypy_django_plugin.plugins.fields import determine_type_of_array_field, record_field_properties_into_outer_model_class
from mypy_django_plugin.plugins.init_create import redefine_and_typecheck_model_init, redefine_and_typecheck_model_create
from mypy_django_plugin.plugins.migrations import determine_model_cls_from_string_for_migrations, get_string_value_from_expr
from mypy_django_plugin.plugins.models import process_model_class
from mypy_django_plugin.plugins.related_fields import extract_to_parameter_as_get_ret_type_for_related_field, reparametrize_with
from mypy_django_plugin.plugins.settings import AddSettingValuesToDjangoConfObject


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


def return_user_model_hook(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    setting_expr = helpers.get_setting_expr(api, 'AUTH_USER_MODEL')
    if setting_expr is None:
        return ctx.default_return_type

    app_label, _, model_class_name = get_string_value_from_expr(setting_expr).rpartition('.')
    if app_label is None:
        return ctx.default_return_type

    model_fullname = helpers.get_model_fullname(app_label, model_class_name,
                                                all_modules=api.modules)
    if model_fullname is None:
        api.fail(f'"{app_label}.{model_class_name}" model class is not imported so far. Try to import it '
                 f'(under if TYPE_CHECKING) at the beginning of the current file',
                 context=ctx.context)
        return ctx.default_return_type

    model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                        all_modules=api.modules)
    if model_info is None or not isinstance(model_info, TypeInfo):
        return ctx.default_return_type
    return TypeType(Instance(model_info, []))



class DjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

        monkeypatch.restore_original_load_graph()
        monkeypatch.restore_original_dependencies_handling()

        config_fpath = os.environ.get('MYPY_DJANGO_CONFIG')
        if config_fpath:
            self.config = Config.from_config_file(config_fpath)
            self.django_settings = self.config.django_settings_module
        else:
            self.config = Config()
            self.django_settings = None

        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            self.django_settings = os.environ['DJANGO_SETTINGS_MODULE']

        settings_modules = ['django.conf.global_settings']
        if self.django_settings:
            settings_modules.append(self.django_settings)

        monkeypatch.add_modules_as_a_source_seed_files(settings_modules)
        monkeypatch.inject_modules_as_dependencies_for_django_conf_settings(settings_modules)

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            if 'django' not in model_sym.node.metadata:
                model_sym.node.metadata['django'] = {
                    'model_bases': {helpers.MODEL_CLASS_FULLNAME: 1}
                }
            return model_sym.node.metadata['django']['model_bases']
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
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
        if fullname == 'django.contrib.auth.get_user_model':
            return return_user_model_hook

        if fullname in {helpers.FOREIGN_KEY_FULLNAME,
                        helpers.ONETOONE_FIELD_FULLNAME,
                        helpers.MANYTOMANY_FIELD_FULLNAME}:
            return extract_to_parameter_as_get_ret_type_for_related_field

        if fullname == 'django.contrib.postgres.fields.array.ArrayField':
            return determine_type_of_array_field

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return determine_proper_manager_type

        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            if sym.node.has_base(helpers.FIELD_FULLNAME):
                return record_field_properties_into_outer_model_class
            if sym.node.metadata.get('django', {}).get('generated_init'):
                return redefine_and_typecheck_model_init

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        manager_classes = self._get_current_manager_bases()
        class_fullname, _, method_name = fullname.rpartition('.')
        if class_fullname in manager_classes and method_name == 'create':
            return redefine_and_typecheck_model_create

        if fullname in {'django.apps.registry.Apps.get_model',
                        'django.db.migrations.state.StateApps.get_model'}:
            return determine_model_cls_from_string_for_migrations
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_current_model_bases():
            return transform_model_class

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            settings_modules = ['django.conf.global_settings']
            if self.django_settings:
                settings_modules.append(self.django_settings)
            return AddSettingValuesToDjangoConfObject(settings_modules,
                                                      self.config.ignore_missing_settings)

        if fullname in self._get_current_manager_bases():
            return transform_manager_class

        return None


def plugin(version):
    return DjangoPlugin
