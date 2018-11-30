from typing import List, Optional, AbstractSet, MutableSet, Set

from mypy.build import BuildManager, Graph, State, PRI_ALL
from mypy.modulefinder import BuildSource


def is_module_present_in_sources(module_name: str, sources: List[BuildSource]):
    return any([source.module == module_name for source in sources])


from mypy import build

old_load_graph = build.load_graph
OldState = build.State
old_sorted_components = build.sorted_components


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


def _extract_dependencies(graph: Graph, state_id: str, visited_modules: Set[str]) -> Set[str]:
    visited_modules.add(state_id)
    dependencies = set(graph[state_id].dependencies)
    for new_dep_id in dependencies.copy():
        if new_dep_id not in visited_modules:
            dependencies.update(_extract_dependencies(graph, new_dep_id, visited_modules))
    return dependencies


def extract_module_dependencies(graph: Graph, state_id: str) -> Set[str]:
    visited_modules = set()
    return _extract_dependencies(graph, state_id, visited_modules=visited_modules)


def process_settings_before_dependants(settings_module: str):
    def patched_sorted_components(graph: Graph,
                                  vertices: Optional[AbstractSet[str]] = None,
                                  pri_max: int = PRI_ALL) -> List[AbstractSet[str]]:
        sccs = old_sorted_components(graph,
                                     vertices=vertices,
                                     pri_max=pri_max)
        for i, scc in enumerate(sccs.copy()):
            if 'django.conf' in scc:
                django_conf_deps = set(extract_module_dependencies(graph, 'django.conf')).union({'django.conf'})
                old_scc_modified = scc.difference(django_conf_deps)
                new_scc = scc.difference(old_scc_modified)
                if not old_scc_modified:
                    # already processed
                    break
                sccs[i] = frozenset(old_scc_modified)
                sccs.insert(i, frozenset(new_scc))
                break
        return sccs

    build.sorted_components = patched_sorted_components
