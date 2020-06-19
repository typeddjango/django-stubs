from mypy_django_plugin.lib import sem_helpers
from mypy_django_plugin.lib.helpers import ClassDefPluginCallback


class FormCallback(ClassDefPluginCallback):
    def modify_class_defn(self) -> None:
        meta_node = sem_helpers.get_nested_meta_node_for_current_class(self.class_defn.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True
