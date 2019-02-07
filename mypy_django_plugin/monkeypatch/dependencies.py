from typing import List, Optional

from mypy import build
from mypy.build import BuildManager, Graph, State
from mypy.modulefinder import BuildSource

old_load_graph = build.load_graph
OldState = build.State


def is_module_present_in_sources(module_name: str, sources: List[BuildSource]):
    return any([source.module == module_name for source in sources])


def add_modules_as_a_source_seed_files(modules: List[str]) -> None:
    def patched_load_graph(sources: List[BuildSource], manager: BuildManager,
                           old_graph: Optional[Graph] = None,
                           new_modules: Optional[List[State]] = None):
        # add global settings
        for module_name in modules:
            if not is_module_present_in_sources(module_name, sources):
                sources.append(BuildSource(None, module_name, None))

        return old_load_graph(sources=sources, manager=manager,
                              old_graph=old_graph,
                              new_modules=new_modules)

    build.load_graph = patched_load_graph


def restore_original_load_graph():
    from mypy import build

    build.load_graph = old_load_graph


def inject_modules_as_dependencies_for_django_conf_settings(modules: List[str]) -> None:
    from mypy import build

    class PatchedState(build.State):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.id == 'django.conf':
                self.dependencies.extend(modules)

    build.State = PatchedState


def restore_original_dependencies_handling():
    from mypy import build

    build.State = OldState
