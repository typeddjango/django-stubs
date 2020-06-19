from mypy.types import Type as MypyType, AnyType, TypeOfAny, Instance, TypeType

from mypy_django_plugin.lib import helpers
from mypy_django_plugin.transformers2 import new_helpers


class GetUserModel(helpers.GetFunctionCallback):
    def get_function_return_type(self) -> MypyType:
        auth_user_model = self.django_context.settings.AUTH_USER_MODEL
        model_cls = self.django_context.apps_registry.get_model(auth_user_model)
        model_cls_fullname = new_helpers.get_class_fullname(model_cls)

        model_info = helpers.lookup_fully_qualified_typeinfo(self.type_checker, model_cls_fullname)
        if model_info is None:
            return AnyType(TypeOfAny.unannotated)

        return TypeType(Instance(model_info, []))
