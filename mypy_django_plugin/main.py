import itertools
import sys
from functools import cached_property, partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from mypy.build import PRI_MED, PRI_MYPY
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
    ReportConfigContext,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.config import DjangoPluginConfig
from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers import (
    fields,
    forms,
    init_create,
    manytomany,
    manytoone,
    meta,
    orm_lookups,
    querysets,
    settings,
)
from mypy_django_plugin.transformers.auth import get_user_model
from mypy_django_plugin.transformers.functional import resolve_str_promise_attribute
from mypy_django_plugin.transformers.managers import (
    add_as_manager_to_queryset_class,
    create_new_manager_class_from_from_queryset_method,
    reparametrize_any_manager_hook,
    resolve_manager_method,
)
from mypy_django_plugin.transformers.models import (
    MetaclassAdjustments,
    handle_annotated_type,
    process_model_class,
    set_auth_user_model_boolean_fields,
)
from mypy_django_plugin.transformers.request import check_querydict_is_mutable


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        bases = helpers.get_django_metadata_bases(sym.node, "baseform_bases")
        bases[ctx.cls.fullname] = 1

    forms.make_meta_nested_class_inherit_from_any(ctx)


class NewSemanalDjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.plugin_config = DjangoPluginConfig(options.config_file)
        # Add paths from MYPYPATH env var
        sys.path.extend(mypy_path())
        # Add paths from mypy_path config option
        sys.path.extend(options.mypy_path)
        self.django_context = DjangoContext(self.plugin_config.django_settings_module)

    def _get_current_queryset_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.QUERYSET_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            bases = helpers.get_django_metadata_bases(model_sym.node, "queryset_bases")
            bases[fullnames.QUERYSET_CLASS_FULLNAME] = 1
            return bases
        else:
            return {}

    def _get_current_form_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.BASEFORM_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            bases = helpers.get_django_metadata_bases(model_sym.node, "baseform_bases")
            bases[fullnames.BASEFORM_CLASS_FULLNAME] = 1
            bases[fullnames.FORM_CLASS_FULLNAME] = 1
            bases[fullnames.MODELFORM_CLASS_FULLNAME] = 1
            return bases
        else:
            return {}

    def _get_typeinfo_or_none(self, class_name: str) -> Optional[TypeInfo]:
        sym = self.lookup_fully_qualified(class_name)
        if sym is not None and isinstance(sym.node, TypeInfo):
            return sym.node
        return None

    def _new_dependency(self, module: str, priority: int = PRI_MYPY) -> Tuple[int, str, int]:
        fake_lineno = -1
        return (priority, module, fake_lineno)

    def get_additional_deps(self, file: MypyFile) -> List[Tuple[int, str, int]]:
        # for settings
        if file.fullname == "django.conf" and self.django_context.django_settings_module:
            return [self._new_dependency(self.django_context.django_settings_module, PRI_MED)]

        # for values / values_list
        if file.fullname == "django.db.models":
            return [self._new_dependency("typing"), self._new_dependency("django_stubs_ext")]

        # for `get_user_model()`
        if file.fullname == "django.contrib.auth" or file.fullname in {"django.http", "django.http.request"}:
            auth_user_model_name = self.django_context.settings.AUTH_USER_MODEL
            try:
                auth_user_module = self.django_context.apps_registry.get_model(auth_user_model_name).__module__
            except LookupError:
                # get_user_model() model app is not installed
                return []
            return [self._new_dependency(auth_user_module), self._new_dependency("django_stubs_ext")]

        # ensure that all mentioned to='someapp.SomeModel' are loaded with corresponding related Fields
        defined_model_classes = self.django_context.model_modules.get(file.fullname)
        if not defined_model_classes:
            return []
        deps = set()

        for model_class in defined_model_classes.values():
            for field in itertools.chain(
                # forward relations
                self.django_context.get_model_related_fields(model_class),
                # reverse relations - `related_objects` is private API (according to docstring)
                model_class._meta.related_objects,  # type: ignore[attr-defined]
            ):
                try:
                    related_model_cls = self.django_context.get_field_related_model_cls(field)
                except UnregisteredModelError:
                    continue
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
        info = self._get_typeinfo_or_none(fullname)
        if info:
            if info.has_base(fullnames.FIELD_FULLNAME):
                return partial(fields.transform_into_proper_return_type, django_context=self.django_context)

            if helpers.is_model_type(info):
                return partial(init_create.redefine_and_typecheck_model_init, django_context=self.django_context)

            if info.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
                return querysets.determine_proper_manager_type

        return None

    @cached_property
    def manager_and_queryset_method_hooks(self) -> Dict[str, Callable[[MethodContext], MypyType]]:
        typecheck_filtering_method = partial(orm_lookups.typecheck_queryset_filter, django_context=self.django_context)
        return {
            "values": partial(querysets.extract_proper_type_queryset_values, django_context=self.django_context),
            "values_list": partial(
                querysets.extract_proper_type_queryset_values_list, django_context=self.django_context
            ),
            "alias": partial(querysets.extract_proper_type_queryset_annotate, django_context=self.django_context),
            "annotate": partial(querysets.extract_proper_type_queryset_annotate, django_context=self.django_context),
            "create": partial(init_create.redefine_and_typecheck_model_create, django_context=self.django_context),
            "filter": typecheck_filtering_method,
            "get": typecheck_filtering_method,
            "exclude": typecheck_filtering_method,
        }

    def get_method_hook(self, fullname: str) -> Optional[Callable[[MethodContext], MypyType]]:
        class_fullname, _, method_name = fullname.rpartition(".")
        # Methods called very often -- short circuit for minor speed up
        if method_name == "__init_subclass__" or fullname.startswith("builtins."):
            return None

        if class_fullname.endswith("QueryDict"):
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYDICT_CLASS_FULLNAME):
                return partial(check_querydict_is_mutable, django_context=self.django_context)

        elif method_name == "get_form_class":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return forms.extract_proper_type_for_get_form_class

        elif method_name == "get_form":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return forms.extract_proper_type_for_get_form

        elif method_name == "__get__":
            hooks = {
                fullnames.MANYTOMANY_FIELD_FULLNAME: manytomany.refine_many_to_many_related_manager,
                fullnames.MANY_TO_MANY_DESCRIPTOR: manytomany.refine_many_to_many_related_manager,
                fullnames.REVERSE_MANY_TO_ONE_DESCRIPTOR: manytoone.refine_many_to_one_related_manager,
            }
            return hooks.get(class_fullname)

        if method_name in self.manager_and_queryset_method_hooks:
            info = self._get_typeinfo_or_none(class_fullname)
            if info and helpers.has_any_of_bases(
                info, [fullnames.QUERYSET_CLASS_FULLNAME, fullnames.MANAGER_CLASS_FULLNAME]
            ):
                return self.manager_and_queryset_method_hooks[method_name]
        elif method_name == "get_field":
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.OPTIONS_CLASS_FULLNAME):
                return partial(meta.return_proper_field_type_from_get_field, django_context=self.django_context)

        return None

    def get_customize_class_mro_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        sym = self.lookup_fully_qualified(fullname)
        if (
            sym is not None
            and isinstance(sym.node, TypeInfo)
            and sym.node.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME)
        ):
            return reparametrize_any_manager_hook
        else:
            return None

    def get_metaclass_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == fullnames.MODEL_METACLASS_FULLNAME:
            return MetaclassAdjustments.adjust_model_class
        return None

    def get_base_class_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        # Base class is a Model class definition
        sym = self.lookup_fully_qualified(fullname)
        if sym is not None and isinstance(sym.node, TypeInfo) and helpers.is_model_type(sym.node):
            return partial(process_model_class, django_context=self.django_context)

        # Base class is a Form class definition
        if fullname in self._get_current_form_bases():
            return transform_form_class

        # Base class is a QuerySet class definition
        if sym is not None and isinstance(sym.node, TypeInfo) and sym.node.has_base(fullnames.QUERYSET_CLASS_FULLNAME):
            return add_as_manager_to_queryset_class
        return None

    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], MypyType]]:
        class_name, _, attr_name = fullname.rpartition(".")

        # Lookup of a settings variable
        if class_name == fullnames.DUMMY_SETTINGS_BASE_CLASS:
            return partial(
                settings.get_type_of_settings_attribute,
                django_context=self.django_context,
                plugin_config=self.plugin_config,
            )

        info = self._get_typeinfo_or_none(class_name)

        # Lookup of the '.is_superuser' attribute
        if info and info.has_base(fullnames.PERMISSION_MIXIN_CLASS_FULLNAME) and attr_name == "is_superuser":
            return partial(set_auth_user_model_boolean_fields, django_context=self.django_context)

        # Lookup of the 'user.is_staff' or 'user.is_active' attribute
        if info and info.has_base(fullnames.ABSTRACT_USER_MODEL_FULLNAME) and attr_name in ("is_staff", "is_active"):
            return partial(set_auth_user_model_boolean_fields, django_context=self.django_context)

        # Lookup of a method on a dynamically generated manager class
        # i.e. a manager class only existing while mypy is running, not collected from the AST
        if (
            info
            and info.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME)
            and "from_queryset_manager" in helpers.get_django_metadata(info)
        ):
            return resolve_manager_method

        if info and info.has_base(fullnames.STR_PROMISE_FULLNAME):
            return resolve_str_promise_attribute

        return None

    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        if fullname in (
            "typing.Annotated",
            "typing_extensions.Annotated",
            "django_stubs_ext.annotations.WithAnnotations",
        ):
            return partial(handle_annotated_type, fullname=fullname)
        elif fullname == "django.contrib.auth.base_user._UserModel":
            return partial(get_user_model, django_context=self.django_context)
        return None

    def get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], None]]:
        # Create a new manager class definition when a manager's '.from_queryset' classmethod is called
        class_name, _, method_name = fullname.rpartition(".")
        if method_name == "from_queryset":
            info = self._get_typeinfo_or_none(class_name)
            if info and info.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
                return create_new_manager_class_from_from_queryset_method
        return None

    def report_config_data(self, ctx: ReportConfigContext) -> Dict[str, Any]:
        # Cache would be cleared if any settings do change.
        extra_data = {}
        # In all places we use '_UserModel' alias as a type we want to clear cache if
        # AUTH_USER_MODEL setting changes
        if ctx.id.startswith("django.contrib.auth") or ctx.id in {"django.http.request", "django.test.client"}:
            extra_data["AUTH_USER_MODEL"] = self.django_context.settings.AUTH_USER_MODEL
        return self.plugin_config.to_json(extra_data)


def plugin(version: str) -> Type[NewSemanalDjangoPlugin]:
    return NewSemanalDjangoPlugin
