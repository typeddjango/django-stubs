import os
from functools import partial
from typing import Callable, Dict, List, Optional, Tuple, Type

import toml
from mypy.nodes import MypyFile, TypeInfo
from mypy.options import Options
from mypy.plugin import ClassDefContext, FunctionContext, Plugin, MethodContext, AttributeContext
from mypy.types import Type as MypyType

from django.db.models.fields.related import RelatedField
from mypy_django_plugin_newsemanal.django.context import DjangoContext
from mypy_django_plugin_newsemanal.lib import fullnames, metadata
from mypy_django_plugin_newsemanal.transformers import fields, settings, querysets, init_create
from mypy_django_plugin_newsemanal.transformers.models import process_model_class


def transform_model_class(ctx: ClassDefContext,
                          django_context: DjangoContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.MODEL_CLASS_FULLNAME)

    if sym is not None and isinstance(sym.node, TypeInfo):
        metadata.get_django_metadata(sym.node)['model_bases'][ctx.cls.fullname] = 1
    else:
        if not ctx.api.final_iteration:
            ctx.api.defer()
            return

    process_model_class(ctx, django_context)


def add_new_manager_base(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.MANAGER_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        metadata.get_django_metadata(sym.node)['manager_bases'][ctx.cls.fullname] = 1


class NewSemanalDjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

        plugin_toml_config = None
        if os.path.exists('pyproject.toml'):
            with open('pyproject.toml', 'r') as f:
                pyproject_toml = toml.load(f)
                plugin_toml_config = pyproject_toml.get('tool', {}).get('django-stubs')

        self.django_context = DjangoContext(plugin_toml_config)

    def _get_current_queryset_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.QUERYSET_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (metadata.get_django_metadata(model_sym.node)
                    .setdefault('queryset_bases', {fullnames.QUERYSET_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MANAGER_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (metadata.get_django_metadata(model_sym.node)
                    .setdefault('manager_bases', {fullnames.MANAGER_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return metadata.get_django_metadata(model_sym.node).setdefault('model_bases',
                                                                           {fullnames.MODEL_CLASS_FULLNAME: 1})
        else:
            return {}

    def _get_typeinfo_or_none(self, class_name: str) -> Optional[TypeInfo]:
        sym = self.lookup_fully_qualified(class_name)
        if sym is not None and isinstance(sym.node, TypeInfo):
            return sym.node
        return None

    def _new_dependency(self, module: str) -> Tuple[int, str, int]:
        return 10, module, -1

    def get_additional_deps(self, file: MypyFile) -> List[Tuple[int, str, int]]:
        # for settings
        if file.fullname() == 'django.conf' and self.django_context.django_settings_module:
            return [self._new_dependency(self.django_context.django_settings_module)]

        # for `get_user_model()`
        if file.fullname() == 'django.contrib.auth':
            auth_user_model_name = self.django_context.settings.AUTH_USER_MODEL
            try:
                auth_user_module = self.django_context.apps_registry.get_model(auth_user_model_name).__module__
            except LookupError:
                # get_user_model() model app is not installed
                return []
            return [self._new_dependency(auth_user_module)]

        # ensure that all mentioned to='someapp.SomeModel' are loaded with corresponding related Fields
        defined_model_classes = self.django_context.model_modules.get(file.fullname())
        if not defined_model_classes:
            return []
        deps = set()
        for model_class in defined_model_classes:
            # forward relations
            for field in self.django_context.get_model_fields(model_class):
                if isinstance(field, RelatedField):
                    related_model_module = field.related_model.__module__
                    if related_model_module != file.fullname():
                        deps.add(self._new_dependency(related_model_module))
            # reverse relations
            for relation in model_class._meta.related_objects:
                related_model_module = relation.related_model.__module__
                if related_model_module != file.fullname():
                    deps.add(self._new_dependency(related_model_module))
        return list(deps)

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], MypyType]]:
        if fullname == 'django.contrib.auth.get_user_model':
            return partial(settings.get_user_model_hook, django_context=self.django_context)

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return querysets.determine_proper_manager_type

        info = self._get_typeinfo_or_none(fullname)
        if info:
            if info.has_base(fullnames.FIELD_FULLNAME):
                return partial(fields.transform_into_proper_return_type, django_context=self.django_context)

            if info.has_base(fullnames.MODEL_CLASS_FULLNAME):
                return partial(init_create.redefine_and_typecheck_model_init, django_context=self.django_context)

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        manager_classes = self._get_current_manager_bases()
        class_fullname, _, method_name = fullname.rpartition('.')
        if class_fullname in manager_classes and method_name == 'create':
            return partial(init_create.redefine_and_typecheck_model_create, django_context=self.django_context)

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_current_model_bases():
            return partial(transform_model_class, django_context=self.django_context)

        if fullname in self._get_current_manager_bases():
            return add_new_manager_base

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], MypyType]]:
        class_name, _, attr_name = fullname.rpartition('.')
        if class_name == fullnames.DUMMY_SETTINGS_BASE_CLASS:
            return partial(settings.get_type_of_settings_attribute,
                           django_context=self.django_context)

    # def get_type_analyze_hook(self, fullname: str
    #                           ) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
    #     queryset_bases = self._get_current_queryset_bases()
    #     if fullname in queryset_bases:
    #         return partial(querysets.set_first_generic_param_as_default_for_second, fullname=fullname)


def plugin(version):
    return NewSemanalDjangoPlugin
