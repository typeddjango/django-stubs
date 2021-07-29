import configparser
import sys
import textwrap
from functools import partial
from typing import Callable, Dict, List, NoReturn, Optional, Tuple, cast

import toml
from django.db.models.fields.related import RelatedField
from mypy.modulefinder import mypy_path
from mypy.nodes import MypyFile, TypeInfo
from mypy.options import Options
from mypy.plugin import (
    AnalyzeTypeContext,
    AttributeContext,
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    MethodContext,
    Plugin,
)
from mypy.types import Type as MypyType

import mypy_django_plugin.transformers.orm_lookups
from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers import fields, forms, init_create, meta, querysets, request, settings
from mypy_django_plugin.transformers.managers import create_new_manager_class_from_from_queryset_method
from mypy_django_plugin.transformers.models import (
    handle_annotated_type,
    process_model_class,
    set_auth_user_model_boolean_fields,
)


def transform_model_class(ctx: ClassDefContext, django_context: DjangoContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.MODEL_CLASS_FULLNAME)

    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_django_metadata(sym.node)["model_bases"][ctx.cls.fullname] = 1
    else:
        if not ctx.api.final_iteration:
            ctx.api.defer()
            return

    process_model_class(ctx, django_context)


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_django_metadata(sym.node)["baseform_bases"][ctx.cls.fullname] = 1

    forms.make_meta_nested_class_inherit_from_any(ctx)


def add_new_manager_base_hook(ctx: ClassDefContext) -> None:
    helpers.add_new_manager_base(ctx.api, ctx.cls.fullname)


def extract_django_settings_module(config_file_path: Optional[str]) -> str:
    def exit(error_type: int) -> NoReturn:
        """Using mypy's argument parser, raise `SystemExit` to fail hard if validation fails.

        Considering that the plugin's startup duration is around double as long as mypy's, this aims to
        import and construct objects only when that's required - which happens once and terminates the
        run. Considering that most of the runs are successful, there's no need for this to linger in the
        global scope.
        """
        from mypy.main import CapturableArgumentParser

        usage = """
        (config)
        ...
        [mypy.plugins.django_stubs]
            django_settings_module: str (required)
        ...
        """
        handler = CapturableArgumentParser(prog="(django-stubs) mypy", usage=textwrap.dedent(usage))
        messages = {
            1: "mypy config file is not specified or found",
            2: "no section [mypy.plugins.django-stubs]",
            3: "the setting is not provided",
        }
        handler.error("'django_settings_module' is not set: " + messages[error_type])

    def exit_toml(error_type: int) -> NoReturn:
        from mypy.main import CapturableArgumentParser

        usage = """
        (config)
        ...
        [tool.django-stubs]
        django_settings_module = str (required)
        ...
        """
        handler = CapturableArgumentParser(prog="(django-stubs) mypy", usage=textwrap.dedent(usage))
        messages = {
            1: "mypy config file is not specified or found",
            2: "no section [tool.django-stubs]",
            3: "the setting is not provided",
            4: "the setting must be a string",
        }
        handler.error("'django_settings_module' not found or invalid: " + messages[error_type])

    if config_file_path and helpers.is_toml(config_file_path):
        toml_data = toml.load(config_file_path)
        try:
            config = toml_data["tool"]["django-stubs"]
        except KeyError:
            exit_toml(2)

        if "django_settings_module" not in config:
            exit_toml(3)

        if not isinstance(config["django_settings_module"], str):
            exit_toml(4)

        return config["django_settings_module"]
    else:
        parser = configparser.ConfigParser()
        try:
            with open(cast(str, config_file_path)) as handle:
                parser.read_file(handle, source=config_file_path)
        except (IsADirectoryError, OSError):
            exit(1)

        section = "mypy.plugins.django-stubs"
        if not parser.has_section(section):
            exit(2)
        settings = parser.get(section, "django_settings_module", fallback=None) or exit(3)

        return settings.strip("'\"")


class NewSemanalDjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        django_settings_module = extract_django_settings_module(options.config_file)
        # Add paths from MYPYPATH env var
        sys.path.extend(mypy_path())
        # Add paths from mypy_path config option
        sys.path.extend(options.mypy_path)
        self.django_context = DjangoContext(django_settings_module)

    def _get_current_queryset_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.QUERYSET_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return helpers.get_django_metadata(model_sym.node).setdefault(
                "queryset_bases", {fullnames.QUERYSET_CLASS_FULLNAME: 1}
            )
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MANAGER_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return helpers.get_django_metadata(model_sym.node).setdefault(
                "manager_bases", {fullnames.MANAGER_CLASS_FULLNAME: 1}
            )
        else:
            return {}

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return helpers.get_django_metadata(model_sym.node).setdefault(
                "model_bases", {fullnames.MODEL_CLASS_FULLNAME: 1}
            )
        else:
            return {}

    def _get_current_form_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.BASEFORM_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return helpers.get_django_metadata(model_sym.node).setdefault(
                "baseform_bases",
                {
                    fullnames.BASEFORM_CLASS_FULLNAME: 1,
                    fullnames.FORM_CLASS_FULLNAME: 1,
                    fullnames.MODELFORM_CLASS_FULLNAME: 1,
                },
            )
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
        if file.fullname == "django.conf" and self.django_context.django_settings_module:
            return [self._new_dependency(self.django_context.django_settings_module)]

        # for values / values_list
        if file.fullname == "django.db.models":
            return [self._new_dependency("mypy_extensions"), self._new_dependency("typing")]

        # for `get_user_model()`
        if self.django_context.settings:
            if file.fullname == "django.contrib.auth" or file.fullname in {"django.http", "django.http.request"}:
                auth_user_model_name = self.django_context.settings.AUTH_USER_MODEL
                try:
                    auth_user_module = self.django_context.apps_registry.get_model(auth_user_model_name).__module__
                except LookupError:
                    # get_user_model() model app is not installed
                    return []
                return [self._new_dependency(auth_user_module)]

        # ensure that all mentioned to='someapp.SomeModel' are loaded with corresponding related Fields
        defined_model_classes = self.django_context.model_modules.get(file.fullname)
        if not defined_model_classes:
            return []
        deps = set()
        for model_class in defined_model_classes:
            # forward relations
            for field in self.django_context.get_model_fields(model_class):
                if isinstance(field, RelatedField):
                    related_model_cls = self.django_context.get_field_related_model_cls(field)
                    if related_model_cls is None:
                        continue
                    related_model_module = related_model_cls.__module__
                    if related_model_module != file.fullname:
                        deps.add(self._new_dependency(related_model_module))
            # reverse relations
            for relation in model_class._meta.related_objects:
                related_model_cls = self.django_context.get_field_related_model_cls(relation)
                related_model_module = related_model_cls.__module__
                if related_model_module != file.fullname:
                    deps.add(self._new_dependency(related_model_module))
        return list(deps) + [
            # for QuerySet.annotate
            self._new_dependency("django_stubs_ext"),
            # For BaseManager.from_queryset
            self._new_dependency("django.db.models.query"),
        ]

    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], MypyType]]:
        if fullname == "django.contrib.auth.get_user_model":
            return partial(settings.get_user_model_hook, django_context=self.django_context)

        manager_bases = self._get_current_manager_bases()
        if fullname in manager_bases:
            return querysets.determine_proper_manager_type

        info = self._get_typeinfo_or_none(fullname)
        if info:
            if info.has_base(fullnames.FIELD_FULLNAME):
                return partial(fields.transform_into_proper_return_type, django_context=self.django_context)

            if helpers.is_model_subclass_info(info, self.django_context):
                return partial(init_create.redefine_and_typecheck_model_init, django_context=self.django_context)
        return None

    def get_method_hook(self, fullname: str) -> Optional[Callable[[MethodContext], MypyType]]:
        class_fullname, _, method_name = fullname.rpartition(".")
        if method_name == "get_form_class":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return forms.extract_proper_type_for_get_form_class

        if method_name == "get_form":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return forms.extract_proper_type_for_get_form

        manager_classes = self._get_current_manager_bases()

        if method_name == "values":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYSET_CLASS_FULLNAME) or class_fullname in manager_classes:
                return partial(querysets.extract_proper_type_queryset_values, django_context=self.django_context)

        if method_name == "values_list":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYSET_CLASS_FULLNAME) or class_fullname in manager_classes:
                return partial(querysets.extract_proper_type_queryset_values_list, django_context=self.django_context)

        if method_name == "annotate":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYSET_CLASS_FULLNAME) or class_fullname in manager_classes:
                return partial(querysets.extract_proper_type_queryset_annotate, django_context=self.django_context)

        if method_name == "get_field":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.OPTIONS_CLASS_FULLNAME):
                return partial(meta.return_proper_field_type_from_get_field, django_context=self.django_context)

        if class_fullname in manager_classes and method_name == "create":
            return partial(init_create.redefine_and_typecheck_model_create, django_context=self.django_context)
        if class_fullname in manager_classes and method_name in {"filter", "get", "exclude"}:
            return partial(
                mypy_django_plugin.transformers.orm_lookups.typecheck_queryset_filter,
                django_context=self.django_context,
            )
        return None

    def get_base_class_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        if (
            fullname in self.django_context.all_registered_model_class_fullnames
            or fullname in self._get_current_model_bases()
        ):
            return partial(transform_model_class, django_context=self.django_context)

        if fullname in self._get_current_manager_bases():
            return add_new_manager_base_hook

        if fullname in self._get_current_form_bases():
            return transform_form_class
        return None

    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], MypyType]]:
        class_name, _, attr_name = fullname.rpartition(".")
        if class_name == fullnames.DUMMY_SETTINGS_BASE_CLASS:
            return partial(settings.get_type_of_settings_attribute, django_context=self.django_context)

        info = self._get_typeinfo_or_none(class_name)
        if info and info.has_base(fullnames.PERMISSION_MIXIN_CLASS_FULLNAME) and attr_name == "is_superuser":
            return partial(set_auth_user_model_boolean_fields, django_context=self.django_context)
        if info and info.has_base(fullnames.HTTPREQUEST_CLASS_FULLNAME) and attr_name == "user":
            return partial(request.set_auth_user_model_as_type_for_request_user, django_context=self.django_context)
        if info and info.has_base(fullnames.ABSTRACT_USER_MODEL_FULLNAME) and attr_name in ("is_staff", "is_active"):
            return partial(set_auth_user_model_boolean_fields, django_context=self.django_context)
        return None

    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        if fullname in (
            "typing.Annotated",
            "typing_extensions.Annotated",
            "django_stubs_ext.annotations.WithAnnotations",
        ):
            return partial(handle_annotated_type, django_context=self.django_context)

    def get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if fullname.endswith("from_queryset"):
            class_name, _, _ = fullname.rpartition(".")
            info = self._get_typeinfo_or_none(class_name)
            if info and info.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
                return create_new_manager_class_from_from_queryset_method
        return None


def plugin(version):
    return NewSemanalDjangoPlugin
