import configparser
from typing import Callable, Dict, List, NoReturn, Optional, Tuple, cast

from django.db.models.fields.related import RelatedField
from mypy.nodes import MypyFile, TypeInfo
from mypy.options import Options
from mypy.plugin import (
    AttributeContext, ClassDefContext, DynamicClassDefContext, FunctionContext, MethodContext, Plugin,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers.fields import FieldContructorCallback
from mypy_django_plugin.transformers.forms import (
    FormCallback, GetFormCallback, GetFormClassCallback,
)
from mypy_django_plugin.transformers.init_create import (
    ModelCreateCallback, ModelInitCallback,
)
from mypy_django_plugin.transformers.managers import (
    ManagerFromQuerySetCallback,
)
from mypy_django_plugin.transformers.meta import MetaGetFieldCallback
from mypy_django_plugin.transformers.models import ModelCallback
from mypy_django_plugin.transformers.orm_lookups import (
    QuerySetFilterTypecheckCallback,
)
from mypy_django_plugin.transformers.querysets import (
    QuerySetValuesCallback, QuerySetValuesListCallback,
)
from mypy_django_plugin.transformers.related_managers import (
    GetRelatedManagerCallback,
)
from mypy_django_plugin.transformers.request import RequestUserModelCallback
from mypy_django_plugin.transformers.settings import (
    GetTypeOfSettingsAttributeCallback, GetUserModelCallback,
)


def extract_django_settings_module(config_file_path: Optional[str]) -> str:

    def exit(error_type: int) -> NoReturn:
        """Using mypy's argument parser, raise `SystemExit` to fail hard if validation fails.

        Considering that the plugin's startup duration is around double as long as mypy's, this aims to
        import and construct objects only when that's required - which happens once and terminates the
        run. Considering that most of the runs are successful, there's no need for this to linger in the
        global scope.
        """
        from mypy.main import CapturableArgumentParser

        usage = """(config)
        ...
        [mypy.plugins.django_stubs]
            django_settings_module: str (required)
        ...
        """.replace("\n" + 8 * " ", "\n")
        handler = CapturableArgumentParser(prog='(django-stubs) mypy', usage=usage)
        messages = {1: 'mypy config file is not specified or found',
                    2: 'no section [mypy.plugins.django-stubs]',
                    3: 'the setting is not provided'}
        handler.error("'django_settings_module' is not set: " + messages[error_type])

    parser = configparser.ConfigParser()
    try:
        parser.read_file(open(cast(str, config_file_path), 'r'), source=config_file_path)
    except (IsADirectoryError, OSError):
        exit(1)

    section = 'mypy.plugins.django-stubs'
    if not parser.has_section(section):
        exit(2)
    settings = parser.get(section, 'django_settings_module', fallback=None) or exit(3)
    return cast(str, settings).strip('\'"')


class NewSemanalDjangoPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        django_settings_module = extract_django_settings_module(options.config_file)
        self.django_context = DjangoContext(django_settings_module)

    def _get_current_queryset_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.QUERYSET_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('queryset_bases', {fullnames.QUERYSET_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_manager_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MANAGER_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('manager_bases', {fullnames.MANAGER_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_current_model_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.MODEL_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return helpers.get_django_metadata(model_sym.node).setdefault('model_bases',
                                                                          {fullnames.MODEL_CLASS_FULLNAME: 1})
        else:
            return {}

    def _get_current_form_bases(self) -> Dict[str, int]:
        model_sym = self.lookup_fully_qualified(fullnames.BASEFORM_CLASS_FULLNAME)
        if model_sym is not None and isinstance(model_sym.node, TypeInfo):
            return (helpers.get_django_metadata(model_sym.node)
                    .setdefault('baseform_bases', {fullnames.BASEFORM_CLASS_FULLNAME: 1,
                                                   fullnames.FORM_CLASS_FULLNAME: 1,
                                                   fullnames.MODELFORM_CLASS_FULLNAME: 1}))
        else:
            return {}

    def _get_typeinfo_or_none(self, class_name: str) -> Optional[TypeInfo]:
        sym = self.lookup_fully_qualified(class_name)
        if sym is not None and isinstance(sym.node, TypeInfo):
            return sym.node
        return None

    def _new_dependency(self, module: str) -> Tuple[int, str, int]:
        return 10, module, -1

    def _add_new_manager_base(self, fullname: str) -> None:
        sym = self.lookup_fully_qualified(fullnames.MANAGER_CLASS_FULLNAME)
        if sym is not None and isinstance(sym.node, TypeInfo):
            helpers.get_django_metadata(sym.node)['manager_bases'][fullname] = 1

    def _add_new_form_base(self, fullname: str) -> None:
        sym = self.lookup_fully_qualified(fullnames.BASEFORM_CLASS_FULLNAME)
        if sym is not None and isinstance(sym.node, TypeInfo):
            helpers.get_django_metadata(sym.node)['baseform_bases'][fullname] = 1

    def get_additional_deps(self, file: MypyFile) -> List[Tuple[int, str, int]]:
        # load QuerySet and Manager together (for as_manager)
        if file.fullname == 'django.db.models.query':
            return [self._new_dependency('django.db.models.manager')]

        # for settings
        if file.fullname == 'django.conf' and self.django_context.django_settings_module:
            return [self._new_dependency(self.django_context.django_settings_module)]

        # for values / values_list
        if file.fullname == 'django.db.models':
            return [self._new_dependency('mypy_extensions'), self._new_dependency('typing')]

        # for `get_user_model()`
        if self.django_context.settings:
            if (file.fullname == 'django.contrib.auth'
                    or file.fullname in {'django.http', 'django.http.request'}):
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
        return list(deps)

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], MypyType]]:
        if fullname == 'django.contrib.auth.get_user_model':
            return GetUserModelCallback(self)

        info = self._get_typeinfo_or_none(fullname)
        if info:
            if info.has_base(fullnames.FIELD_FULLNAME):
                return FieldContructorCallback(self)

            if self.django_context.is_model_subclass(info):
                return ModelInitCallback(self)
        return None

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], MypyType]]:
        class_fullname, _, method_name = fullname.rpartition('.')
        if method_name == 'get_form_class':
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return GetFormClassCallback(self)

        if method_name == 'get_form':
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.FORM_MIXIN_CLASS_FULLNAME):
                return GetFormCallback(self)

        if method_name == 'values':
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYSET_CLASS_FULLNAME):
                return QuerySetValuesCallback(self)
                # return partial(querysets.extract_proper_type_queryset_values, django_context=self.django_context)

        if method_name == 'values_list':
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.QUERYSET_CLASS_FULLNAME):
                return QuerySetValuesListCallback(self)
                # return partial(querysets.extract_proper_type_queryset_values_list, django_context=self.django_context)

        if method_name == 'get_field':
            info = self._get_typeinfo_or_none(class_fullname)
            if info and info.has_base(fullnames.OPTIONS_CLASS_FULLNAME):
                return MetaGetFieldCallback(self)

        manager_classes = self._get_current_manager_bases()
        if class_fullname in manager_classes and method_name == 'create':
            return ModelCreateCallback(self)

        if class_fullname in manager_classes and method_name in {'filter', 'get', 'exclude'}:
            return QuerySetFilterTypecheckCallback(self)

        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if (fullname in self.django_context.all_registered_model_class_fullnames
                or fullname in self._get_current_model_bases()):
            return ModelCallback(self)

        if fullname in self._get_current_manager_bases():
            self._add_new_manager_base(fullname)
            return None

        if fullname in self._get_current_form_bases():
            self._add_new_form_base(fullname)
            return FormCallback(self)

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], MypyType]]:
        class_name, _, attr_name = fullname.rpartition('.')
        if class_name == fullnames.DUMMY_SETTINGS_BASE_CLASS:
            return GetTypeOfSettingsAttributeCallback(self)

        info = self._get_typeinfo_or_none(class_name)
        if info and info.has_base(fullnames.HTTPREQUEST_CLASS_FULLNAME) and attr_name == 'user':
            return RequestUserModelCallback(self)

        if info and info.has_base(fullnames.MODEL_CLASS_FULLNAME):
            return GetRelatedManagerCallback(self)

        return None

    def get_dynamic_class_hook(self, fullname: str
                               ) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if fullname.endswith('from_queryset'):
            class_name, _, _ = fullname.rpartition('.')
            info = self._get_typeinfo_or_none(class_name)
            if info and info.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
                return ManagerFromQuerySetCallback(self)
        return None


def plugin(version):
    return NewSemanalDjangoPlugin
