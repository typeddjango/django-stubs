import os
from typing import Callable, Optional, Set, Union, cast, Dict

from mypy.checker import TypeChecker
from mypy.nodes import MemberExpr, TypeInfo
from mypy.options import Options
from mypy.plugin import AttributeContext, ClassDefContext, FunctionContext, MethodContext, Plugin
from mypy.types import AnyType, Instance, Type, TypeOfAny, TypeType, UnionType
from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.config import Config
from mypy_django_plugin.transformers import fields, init_create
from mypy_django_plugin.transformers.forms import make_meta_nested_class_inherit_from_any
from mypy_django_plugin.transformers.migrations import determine_model_cls_from_string_for_migrations, \
    get_string_value_from_expr
from mypy_django_plugin.transformers.models import process_model_class
from mypy_django_plugin.transformers.settings import AddSettingValuesToDjangoConfObject, get_settings_metadata


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


def transform_modelform_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.MODELFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['modelform_bases'][ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)


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
            ret.type.bases[i] = Instance(base.type, [Instance(outer_model_info, [])])
            return ret
    return ret


def return_user_model_hook(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    setting_expr = helpers.get_setting_expr(api, 'AUTH_USER_MODEL')
    if setting_expr is None:
        return ctx.default_return_type

    model_path = get_string_value_from_expr(setting_expr)
    if model_path is None:
        return ctx.default_return_type

    app_label, _, model_class_name = model_path.rpartition('.')
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


def _extract_referred_to_type_info(typ: Union[UnionType, Instance]) -> Optional[TypeInfo]:
    if isinstance(typ, Instance):
        return typ.type
    else:
        # should be Union[TYPE, None]
        typ = helpers.make_required(typ)
        if isinstance(typ, Instance):
            return typ.type
    return None


def extract_and_return_primary_key_of_bound_related_field_parameter(ctx: AttributeContext) -> Type:
    if not isinstance(ctx.default_attr_type, Instance) or not (ctx.default_attr_type.type.fullname() == 'builtins.int'):
        return ctx.default_attr_type

    if not isinstance(ctx.type, Instance) or not ctx.type.type.has_base(helpers.MODEL_CLASS_FULLNAME):
        return ctx.default_attr_type

    field_name = ctx.context.name.split('_')[0]
    sym = ctx.type.type.get(field_name)
    if sym and isinstance(sym.type, Instance) and len(sym.type.args) > 0:
        referred_to = sym.type.args[1]
        if isinstance(referred_to, AnyType):
            return AnyType(TypeOfAny.implementation_artifact)

        model_type = _extract_referred_to_type_info(referred_to)
        if model_type is None:
            return AnyType(TypeOfAny.implementation_artifact)

        primary_key_type = helpers.extract_primary_key_type_for_get(model_type)
        if primary_key_type:
            return primary_key_type

    is_nullable = helpers.get_fields_metadata(ctx.type.type).get(field_name, {}).get('null', False)
    if is_nullable:
        return helpers.make_optional(ctx.default_attr_type)

    return ctx.default_attr_type


def return_integer_type_for_id_for_non_defined_primary_key_in_models(ctx: AttributeContext) -> Type:
    if isinstance(ctx.type, Instance) and ctx.type.type.has_base(helpers.MODEL_CLASS_FULLNAME):
        return ctx.api.named_generic_type('builtins.int', [])
    return ctx.default_attr_type


class ExtractSettingType:
    def __init__(self, module_fullname: str):
        self.module_fullname = module_fullname

    def __call__(self, ctx: AttributeContext) -> Type:
        api = cast(TypeChecker, ctx.api)
        original_module = api.modules.get(self.module_fullname)
        if original_module is None:
            return ctx.default_attr_type

        definition = ctx.context
        if isinstance(definition, MemberExpr):
            sym = original_module.names.get(definition.name)
            if sym and sym.type:
                return sym.type

        return ctx.default_attr_type


class DjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

        monkeypatch.restore_original_load_graph()
        monkeypatch.restore_original_dependencies_handling()

        config_fpath = os.environ.get('MYPY_DJANGO_CONFIG', 'mypy_django.ini')
        if config_fpath and os.path.exists(config_fpath):
            self.config = Config.from_config_file(config_fpath)
            self.django_settings_module = self.config.django_settings_module
        else:
            self.config = Config()
            self.django_settings_module = None

        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            self.django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']

        settings_modules = ['django.conf.global_settings']
        if self.django_settings_module:
            settings_modules.append(self.django_settings_module)

        monkeypatch.add_modules_as_a_source_seed_files(settings_modules)
        monkeypatch.inject_modules_as_dependencies_for_django_conf_settings(settings_modules)

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (model_sym.node.metadata
                    .setdefault('django', {})
                    .setdefault('model_bases', {helpers.MODEL_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MANAGER_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (model_sym.node.metadata
                    .setdefault('django', {})
                    .setdefault('manager_bases', {helpers.MANAGER_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_modelform_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MODELFORM_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (model_sym.node.metadata
                    .setdefault('django', {})
                    .setdefault('modelform_bases', {helpers.MODELFORM_CLASS_FULLNAME: 1}))
        else:
            return {}

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo) and sym.node.has_base(helpers.FIELD_FULLNAME):
            return fields.adjust_return_type_of_field_instantiation

        if fullname == 'django.contrib.auth.get_user_model':
            return return_user_model_hook

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return determine_proper_manager_type

        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            if sym.node.metadata.get('django', {}).get('generated_init'):
                return init_create.redefine_and_typecheck_model_init

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        manager_classes = self._get_current_manager_bases()
        class_fullname, _, method_name = fullname.rpartition('.')
        if class_fullname in manager_classes and method_name == 'create':
            return init_create.redefine_and_typecheck_model_create

        if fullname in {'django.apps.registry.Apps.get_model',
                        'django.db.migrations.state.StateApps.get_model'}:
            return determine_model_cls_from_string_for_migrations
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_current_model_bases():
            return transform_model_class

        if fullname in self._get_current_manager_bases():
            return transform_manager_class

        if fullname in self._get_current_modelform_bases():
            return transform_modelform_class

        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            settings_modules = ['django.conf.global_settings']
            if self.django_settings_module:
                settings_modules.append(self.django_settings_module)
            return AddSettingValuesToDjangoConfObject(settings_modules,
                                                      self.config.ignore_missing_settings)

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        module, _, name = fullname.rpartition('.')
        sym = self.lookup_fully_qualified('django.conf.LazySettings')
        if sym and isinstance(sym.node, TypeInfo):
            metadata = get_settings_metadata(sym.node)
            if module == 'builtins.object' and name in metadata:
                return ExtractSettingType(module_fullname=metadata[name])

        if fullname == 'builtins.object.id':
            return return_integer_type_for_id_for_non_defined_primary_key_in_models

        return extract_and_return_primary_key_of_bound_related_field_parameter


def plugin(version):
    return DjangoPlugin
