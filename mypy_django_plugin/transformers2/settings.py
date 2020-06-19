from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, TypeType

from mypy_django_plugin.lib import helpers
from mypy_django_plugin.transformers2 import new_helpers


class GetUserModelCallback(helpers.GetFunctionCallback):
    def get_function_return_type(self) -> MypyType:
        auth_user_model = self.django_context.settings.AUTH_USER_MODEL
        model_cls = self.django_context.apps_registry.get_model(auth_user_model)
        model_cls_fullname = new_helpers.get_class_fullname(model_cls)

        model_info = helpers.lookup_fully_qualified_typeinfo(self.type_checker, model_cls_fullname)
        if model_info is None:
            return AnyType(TypeOfAny.unannotated)

        return TypeType(Instance(model_info, []))


class GetTypeOfSettingsAttributeCallback(helpers.GetAttributeCallback):
    def get_attribute_type(self) -> MypyType:
        if not hasattr(self.django_context.settings, self.name):
            self.type_checker.fail(f"'Settings' object has no attribute {self.name!r}", self.ctx.context)
            return self.default_attr_type

        # first look for the setting in the project settings file, then global settings
        settings_module = self.type_checker.modules.get(self.django_context.django_settings_module)
        global_settings_module = self.type_checker.modules.get('django.conf.global_settings')
        for module in [settings_module, global_settings_module]:
            if module is not None:
                sym = module.names.get(self.name)
                if sym is not None and sym.type is not None:
                    return sym.type

        # if by any reason it isn't present there, get type from django settings
        value = getattr(self.django_context.settings, self.name)
        value_fullname = helpers.get_class_fullname(value.__class__)

        value_info = helpers.lookup_fully_qualified_typeinfo(self.type_checker, value_fullname)
        if value_info is None:
            return self.default_attr_type

        return Instance(value_info, [])
