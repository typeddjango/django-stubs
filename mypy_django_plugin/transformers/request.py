from mypy.types import Instance
from mypy.types import Type as MypyType
from mypy.types import UnionType

from mypy_django_plugin.lib import helpers


class RequestUserModelCallback(helpers.GetAttributeCallback):
    def get_attribute_type(self) -> MypyType:
        auth_user_model = self.django_context.settings.AUTH_USER_MODEL
        user_cls = self.django_context.apps_registry.get_model(auth_user_model)
        user_info = helpers.lookup_class_typeinfo(self.type_checker, user_cls)

        if user_info is None:
            return self.default_attr_type

        # Imported here because django isn't properly loaded yet when module is loaded
        from django.contrib.auth.models import AnonymousUser

        anonymous_user_info = helpers.lookup_class_typeinfo(self.type_checker, AnonymousUser)
        if anonymous_user_info is None:
            # This shouldn't be able to happen, as we managed to import the model above...
            return Instance(user_info, [])

        return UnionType([Instance(user_info, []), Instance(anonymous_user_info, [])])
