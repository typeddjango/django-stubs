from typing import Optional, Callable

from mypy.plugin import AttributeContext
from mypy.types import Type, Instance

from mypy_django_plugin.helpers import lookup_django_model
from mypy_django_plugin.model_classes import DjangoModelsRegistry
from mypy_django_plugin.plugins.base import BaseDjangoModelsPlugin

# mapping between field types and plain python types
DB_FIELDS_TO_TYPES = {
    'django.db.models.fields.CharField': 'builtins.str',
    'django.db.models.fields.TextField': 'builtins.str',
    'django.db.models.fields.BooleanField': 'builtins.bool',
    # 'django.db.models.fields.NullBooleanField': 'typing.Optional[builtins.bool]',
    'django.db.models.fields.IntegerField': 'builtins.int',
    'django.db.models.fields.AutoField': 'builtins.int',
    'django.db.models.fields.FloatField': 'builtins.float',
    'django.contrib.postgres.fields.jsonb.JSONField': 'builtins.dict',
    'django.contrib.postgres.fields.array.ArrayField': 'typing.Iterable'
}


class DetermineFieldPythonTypeCallback(object):
    def __init__(self, models_registry: DjangoModelsRegistry):
        self.models_registry = models_registry

    def __call__(self, attr_context: AttributeContext) -> Type:
        default_attr_type = attr_context.default_attr_type

        if isinstance(default_attr_type, Instance):
            attr_type_fullname = default_attr_type.type.fullname()
            if attr_type_fullname in DB_FIELDS_TO_TYPES:
                return attr_context.api.named_type(DB_FIELDS_TO_TYPES[attr_type_fullname])

            if 'base' in default_attr_type.type.metadata:
                referred_base_model = default_attr_type.type.metadata['base']
                try:
                    node = lookup_django_model(attr_context.api, referred_base_model).node
                    return Instance(node, [])
                except AssertionError as e:
                    print(e)
                    print('name to lookup:', referred_base_model)
                    pass

        return default_attr_type


class FieldToPythonTypePlugin(BaseDjangoModelsPlugin):
    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        classname, _, attrname = fullname.rpartition('.')
        if classname and classname in self.model_registry:
            return DetermineFieldPythonTypeCallback(self.model_registry)

        return None


def plugin(version):
    return FieldToPythonTypePlugin
