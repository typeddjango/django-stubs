from typing import List, Optional

from mypy.build import BuildManager, Graph, State
from mypy.modulefinder import BuildSource


def is_module_present_in_sources(module_name: str, sources: List[BuildSource]):
    return any([source.module == module_name for source in sources])


from mypy import build

old_load_graph = build.load_graph
OldState = build.State


def load_graph_to_add_settings_file_as_a_source_seed(settings_module: str):
    def patched_load_graph(sources: List[BuildSource], manager: BuildManager,
                           old_graph: Optional[Graph] = None,
                           new_modules: Optional[List[State]] = None):
        if not is_module_present_in_sources(settings_module, sources):
            sources.append(BuildSource(None, settings_module, None))

        return old_load_graph(sources=sources, manager=manager,
                              old_graph=old_graph,
                              new_modules=new_modules)

    build.load_graph = patched_load_graph


def restore_original_load_graph():
    from mypy import build

    build.load_graph = old_load_graph


def inject_dependencies(settings_module: str):
    from mypy import build

    class PatchedState(build.State):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.id == 'django.conf':
                self.dependencies.append(settings_module)

    build.State = PatchedState


def restore_original_dependencies_handling():
    from mypy import build

    build.State = OldState
