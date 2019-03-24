import os
from functools import partial
from typing import Callable, Dict, Optional, Union, cast

from mypy.checker import TypeChecker
from mypy.nodes import MemberExpr, NameExpr, TypeInfo
from mypy.options import Options
from mypy.plugin import (
    AttributeContext, ClassDefContext, FunctionContext, MethodContext, Plugin,
    AnalyzeTypeContext)
from mypy.types import (
    AnyType, CallableType, Instance, NoneTyp, Type, TypeOfAny, TypeType, UnionType,
)

from mypy_django_plugin import helpers, monkeypatch
from mypy_django_plugin.config import Config
from mypy_django_plugin.transformers import fields, init_create
from mypy_django_plugin.transformers.forms import (
    make_meta_nested_class_inherit_from_any,
)
from mypy_django_plugin.transformers.migrations import (
    determine_model_cls_from_string_for_migrations, get_string_value_from_expr,
)
from mypy_django_plugin.transformers.models import process_model_class
from mypy_django_plugin.transformers.queryset import extract_proper_type_for_values_and_values_list
from mypy_django_plugin.transformers.settings import (
    AddSettingValuesToDjangoConfObject, get_settings_metadata,
)


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


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['baseform_bases'][ctx.cls.fullname] = 1

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

    has_manager_base = False
    for i, base in enumerate(ret.type.bases):
        if base.type.fullname() in {helpers.MANAGER_CLASS_FULLNAME,
                                    helpers.RELATED_MANAGER_CLASS_FULLNAME,
                                    helpers.BASE_MANAGER_CLASS_FULLNAME}:
            has_manager_base = True
            break

    if has_manager_base:
        # Fill in the manager's type argument from the outer model
        new_type_args = [Instance(outer_model_info, [])]
        return helpers.reparametrize_instance(ret, new_type_args)
    else:
        return ret


def set_first_generic_param_as_default_for_second(fullname: str, ctx: AnalyzeTypeContext) -> Type:
    if not ctx.type.args:
        try:
            return ctx.api.named_type(fullname, [AnyType(TypeOfAny.explicit),
                                                 AnyType(TypeOfAny.explicit)])
        except KeyError:
            # really should never happen
            return AnyType(TypeOfAny.explicit)

    args = ctx.type.args
    if len(args) == 1:
        args = [args[0], args[0]]

    analyzed_args = [ctx.api.analyze_type(arg) for arg in args]
    try:
        return ctx.api.named_type(fullname, analyzed_args)
    except KeyError:
        # really should never happen
        return AnyType(TypeOfAny.explicit)


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

    is_nullable = helpers.is_field_nullable(ctx.type.type, field_name)
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


def transform_form_view(ctx: ClassDefContext) -> None:
    form_class_value = helpers.get_assigned_value_for_class(ctx.cls.info, 'form_class')
    if isinstance(form_class_value, NameExpr):
        helpers.get_django_metadata(ctx.cls.info)['form_class'] = form_class_value.fullname


def extract_proper_type_for_get_form_class(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    form_class_fullname = helpers.get_django_metadata(object_type.type).get('form_class', None)
    if not form_class_fullname:
        return ctx.default_return_type

    return TypeType(ctx.api.named_generic_type(form_class_fullname, []))


def extract_proper_type_for_get_form(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    form_class_type = helpers.get_argument_type_by_name(ctx, 'form_class')
    if form_class_type is None or isinstance(form_class_type, NoneTyp):
        # extract from specified form_class in metadata
        form_class_fullname = helpers.get_django_metadata(object_type.type).get('form_class', None)
        if not form_class_fullname:
            return ctx.default_return_type

        return ctx.api.named_generic_type(form_class_fullname, [])

    if isinstance(form_class_type, TypeType) and isinstance(form_class_type.item, Instance):
        return form_class_type.item

    if isinstance(form_class_type, CallableType) and isinstance(form_class_type.ret_type, Instance):
        return form_class_type.ret_type

    return ctx.default_return_type


def extract_proper_type_for_values_list(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    flat = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'flat'))
    named = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'named'))

    ret = ctx.default_return_type

    any_type = AnyType(TypeOfAny.implementation_artifact)
    if named and flat:
        ctx.api.fail("'flat' and 'named' can't be used together.", ctx.context)
        return ret
    elif named:
        # TODO: Fill in namedtuple fields/types
        row_arg = ctx.api.named_generic_type('typing.NamedTuple', [])
    elif flat:
        # TODO: Figure out row_arg type dependent on the argument passed in
        if len(ctx.args[0]) > 1:
            ctx.api.fail("'flat' is not valid when values_list is called with more than one field.", ctx.context)
            return ret
        row_arg = any_type
    else:
        # TODO: Figure out tuple argument types dependent on the arguments passed in
        row_arg = ctx.api.named_generic_type('builtins.tuple', [any_type])

    first_arg = ret.args[0] if len(ret.args) > 0 else any_type
    new_type_args = [first_arg, row_arg]
    return helpers.reparametrize_instance(ret, new_type_args)


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

        auto_imports = ['mypy_extensions']
        auto_imports.extend(settings_modules)

        monkeypatch.add_modules_as_a_source_seed_files(auto_imports)
        monkeypatch.inject_modules_as_dependencies_for_django_conf_settings(settings_modules)

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('model_bases', {helpers.MODEL_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.MANAGER_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('manager_bases', {helpers.MANAGER_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_form_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.BASEFORM_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('baseform_bases', {helpers.BASEFORM_CLASS_FULLNAME: 1,
                                                   helpers.FORM_CLASS_FULLNAME: 1,
                                                   helpers.MODELFORM_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_queryset_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(helpers.QUERYSET_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('queryset_bases', {helpers.QUERYSET_CLASS_FULLNAME: 1}))
        else:
            return {}

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.contrib.auth.get_user_model':
            return return_user_model_hook

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return determine_proper_manager_type

        sym = self.lookup_fully_qualified(fullname)
        if sym is not None and isinstance(sym.node, TypeInfo):
            if sym.node.has_base(helpers.FIELD_FULLNAME):
                return fields.adjust_return_type_of_field_instantiation

            if sym.node.metadata.get('django', {}).get('generated_init'):
                return init_create.redefine_and_typecheck_model_init

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        class_name, _, method_name = fullname.rpartition('.')
        if method_name == 'get_form_class':
            sym = self.lookup_fully_qualified(class_name)
            if sym and isinstance(sym.node, TypeInfo) and sym.node.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
                return extract_proper_type_for_get_form_class

        if method_name == 'get_form':
            sym = self.lookup_fully_qualified(class_name)
            if sym and isinstance(sym.node, TypeInfo) and sym.node.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
                return extract_proper_type_for_get_form

        if method_name in ('values', 'values_list'):
            sym = self.lookup_fully_qualified(class_name)
            if sym and isinstance(sym.node, TypeInfo) and sym.node.has_base(helpers.QUERYSET_CLASS_FULLNAME):
                return partial(extract_proper_type_for_values_and_values_list, method_name)

        if fullname in {'django.apps.registry.Apps.get_model',
                        'django.db.migrations.state.StateApps.get_model'}:
            return determine_model_cls_from_string_for_migrations

        manager_classes = self._get_current_manager_bases()
        class_fullname, _, method_name = fullname.rpartition('.')
        if class_fullname in manager_classes and method_name == 'create':
            return init_create.redefine_and_typecheck_model_create
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == helpers.DUMMY_SETTINGS_BASE_CLASS:
            settings_modules = ['django.conf.global_settings']
            if self.django_settings_module:
                settings_modules.append(self.django_settings_module)
            return AddSettingValuesToDjangoConfObject(settings_modules,
                                                      self.config.ignore_missing_settings)

        if fullname in self._get_current_model_bases():
            return transform_model_class

        if fullname in self._get_current_manager_bases():
            return transform_manager_class

        if fullname in self._get_current_form_bases():
            return transform_form_class

        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo) and sym.node.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
            return transform_form_view

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        if fullname == 'builtins.object.id':
            return return_integer_type_for_id_for_non_defined_primary_key_in_models

        module, _, name = fullname.rpartition('.')
        sym = self.lookup_fully_qualified('django.conf.LazySettings')
        if sym and isinstance(sym.node, TypeInfo):
            metadata = get_settings_metadata(sym.node)
            if module == 'builtins.object' and name in metadata:
                return ExtractSettingType(module_fullname=metadata[name])

        return extract_and_return_primary_key_of_bound_related_field_parameter

    def get_type_analyze_hook(self, fullname: str
                              ) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        queryset_bases = self._get_current_queryset_bases()
        if fullname in queryset_bases:
            return partial(set_first_generic_param_as_default_for_second, fullname)

        return None


def plugin(version):
    return DjangoPlugin
