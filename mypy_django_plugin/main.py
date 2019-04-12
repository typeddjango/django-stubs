import os
from functools import partial
from typing import Callable, Dict, List, Optional, Tuple, cast

from mypy.nodes import MypyFile, NameExpr, TypeInfo
from mypy.options import Options
from mypy.plugin import (
    AnalyzeTypeContext, AttributeContext, ClassDefContext, FunctionContext, MethodContext, Plugin,
)
from mypy.types import AnyType, Instance, Type, TypeOfAny

from mypy_django_plugin import helpers
from mypy_django_plugin.config import Config
from mypy_django_plugin.transformers import fields, init_create
from mypy_django_plugin.transformers.forms import (
    extract_proper_type_for_get_form, extract_proper_type_for_get_form_class, make_meta_nested_class_inherit_from_any,
)
from mypy_django_plugin.transformers.migrations import (
    determine_model_cls_from_string_for_migrations,
)
from mypy_django_plugin.transformers.models import process_model_class
from mypy_django_plugin.transformers.queryset import (
    extract_proper_type_for_queryset_values, extract_proper_type_queryset_values_list,
    set_first_generic_param_as_default_for_second,
)
from mypy_django_plugin.transformers.related import (
    determine_type_of_related_manager, extract_and_return_primary_key_of_bound_related_field_parameter,
)
from mypy_django_plugin.transformers.settings import (
    get_type_of_setting, return_user_model_hook,
)


def transform_model_class(ctx: ClassDefContext, ignore_missing_model_attributes: bool) -> None:
    try:
        sym = ctx.api.lookup_fully_qualified(helpers.MODEL_CLASS_FULLNAME)
    except KeyError:
        # models.Model is not loaded, skip metadata model write
        pass
    else:
        if sym is not None and isinstance(sym.node, TypeInfo):
            helpers.get_django_metadata(sym.node)['model_bases'][ctx.cls.fullname] = 1

    process_model_class(ctx, ignore_missing_model_attributes)


def transform_manager_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.MANAGER_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_django_metadata(sym.node)['manager_bases'][ctx.cls.fullname] = 1


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_django_metadata(sym.node)['baseform_bases'][ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)


def determine_proper_manager_type(ctx: FunctionContext) -> Type:
    from mypy.checker import TypeChecker

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


def return_type_for_id_field(ctx: AttributeContext) -> Type:
    if not isinstance(ctx.type, Instance):
        return AnyType(TypeOfAny.from_error)

    model_info = ctx.type.type  # type: TypeInfo
    primary_key_field_name = helpers.get_primary_key_field_name(model_info)
    if not primary_key_field_name:
        # no field with primary_key=True, just return id as int
        return ctx.api.named_generic_type('builtins.int', [])

    if primary_key_field_name != 'id':
        # there's field with primary_key=True, but it's name is not 'id', fail
        ctx.api.fail("Default primary key 'id' is not defined", ctx.context)
        return AnyType(TypeOfAny.from_error)

    primary_key_sym = model_info.get(primary_key_field_name)
    if primary_key_sym and isinstance(primary_key_sym.type, Instance):
        pass

    # try to parse field type out of primary key field
    field_type = helpers.extract_field_getter_type(primary_key_sym.type)
    if field_type:
        return field_type

    return primary_key_sym.type


def transform_form_view(ctx: ClassDefContext) -> None:
    form_class_value = helpers.get_assigned_value_for_class(ctx.cls.info, 'form_class')
    if isinstance(form_class_value, NameExpr):
        helpers.get_django_metadata(ctx.cls.info)['form_class'] = form_class_value.fullname


class DjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

        config_fpath = os.environ.get('MYPY_DJANGO_CONFIG', 'mypy_django.ini')
        if config_fpath and os.path.exists(config_fpath):
            self.config = Config.from_config_file(config_fpath)
            self.django_settings_module = self.config.django_settings_module
        else:
            self.config = Config()
            self.django_settings_module = None

        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            self.django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']

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

    def _get_settings_modules_in_order_of_priority(self) -> List[str]:
        settings_modules = []
        if self.django_settings_module:
            settings_modules.append(self.django_settings_module)

        settings_modules.append('django.conf.global_settings')
        return settings_modules

    def _get_typeinfo_or_none(self, class_name: str) -> Optional[TypeInfo]:
        sym = self.lookup_fully_qualified(class_name)
        if sym is not None and isinstance(sym.node, TypeInfo):
            return sym.node
        return None

    def get_additional_deps(self, file: MypyFile) -> List[Tuple[int, str, int]]:
        if file.fullname() == 'django.conf' and self.django_settings_module:
            return [(10, self.django_settings_module, -1)]

        if file.fullname() == 'django.db.models.query':
            return [(10, 'mypy_extensions', -1)]

        return []

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.contrib.auth.get_user_model':
            return partial(return_user_model_hook,
                           settings_modules=self._get_settings_modules_in_order_of_priority())

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return determine_proper_manager_type

        info = self._get_typeinfo_or_none(fullname)
        if info:
            if info.has_base(helpers.FIELD_FULLNAME):
                return fields.adjust_return_type_of_field_instantiation

            if helpers.get_django_metadata(info).get('generated_init'):
                return init_create.redefine_and_typecheck_model_init

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        class_name, _, method_name = fullname.rpartition('.')

        if method_name == 'get_form_class':
            info = self._get_typeinfo_or_none(class_name)
            if info and info.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
                return extract_proper_type_for_get_form_class

        if method_name == 'get_form':
            info = self._get_typeinfo_or_none(class_name)
            if info and info.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
                return extract_proper_type_for_get_form

        if method_name == 'values':
            model_info = self._get_typeinfo_or_none(class_name)
            if model_info and model_info.has_base(helpers.QUERYSET_CLASS_FULLNAME):
                return extract_proper_type_for_queryset_values

        if method_name == 'values_list':
            model_info = self._get_typeinfo_or_none(class_name)
            if model_info and model_info.has_base(helpers.QUERYSET_CLASS_FULLNAME):
                return extract_proper_type_queryset_values_list

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
        if fullname in self._get_current_model_bases():
            return partial(transform_model_class,
                           ignore_missing_model_attributes=self.config.ignore_missing_model_attributes)

        if fullname in self._get_current_manager_bases():
            return transform_manager_class

        if fullname in self._get_current_form_bases():
            return transform_form_class

        info = self._get_typeinfo_or_none(fullname)
        if info and info.has_base(helpers.FORM_MIXIN_CLASS_FULLNAME):
            return transform_form_view

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        class_name, _, attr_name = fullname.rpartition('.')
        if class_name == helpers.DUMMY_SETTINGS_BASE_CLASS:
            return partial(get_type_of_setting,
                           setting_name=attr_name,
                           settings_modules=self._get_settings_modules_in_order_of_priority(),
                           ignore_missing_settings=self.config.ignore_missing_settings)

        if class_name in self._get_current_model_bases():
            if attr_name == 'id':
                return return_type_for_id_field

            model_info = self._get_typeinfo_or_none(class_name)
            if model_info:
                related_managers = helpers.get_related_managers_metadata(model_info)
                if attr_name in related_managers:
                    return partial(determine_type_of_related_manager,
                                   related_manager_name=attr_name)

            if attr_name.endswith('_id'):
                return extract_and_return_primary_key_of_bound_related_field_parameter

    def get_type_analyze_hook(self, fullname: str
                              ) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        queryset_bases = self._get_current_queryset_bases()
        if fullname in queryset_bases:
            return partial(set_first_generic_param_as_default_for_second, fullname)

        return None


def plugin(version):
    return DjangoPlugin
