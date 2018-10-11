from typing import Optional, Callable, Type

from mypy.plugin import Plugin, ClassDefContext, AttributeContext

from mypy_django_plugin.model_classes import DjangoModelsRegistry
from mypy_django_plugin.plugins.callbacks import CollectModelsInformationCallback, DetermineFieldPythonTypeCallback


class FieldToPythonTypePlugin(Plugin):
    model_registry = DjangoModelsRegistry()

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self.model_registry:
            return CollectModelsInformationCallback(self.model_registry)

        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        # print(fullname)
        classname, _, attrname = fullname.rpartition('.')
        if classname and classname in self.model_registry:
            return DetermineFieldPythonTypeCallback(self.model_registry)

        return None


def plugin(version):
    return FieldToPythonTypePlugin
