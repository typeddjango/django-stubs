from typing import Optional, List, Sequence

from mypy.build import BuildManager, Graph, State
from mypy.modulefinder import BuildSource
from mypy.nodes import Expression, Context
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import Type, CallableType, Instance


def state_compute_dependencies_to_parse_installed_apps_setting_in_settings_module(settings_module: str,
                                                                                  models_py_modules: List[str]):
    from mypy.build import State

    old_compute_dependencies = State.compute_dependencies

    def patched_compute_dependencies(self: State):
        old_compute_dependencies(self)
        if self.id == settings_module:
            self.dependencies.extend(models_py_modules)

    State.compute_dependencies = patched_compute_dependencies


def load_graph_to_add_settings_file_as_a_source_seed(settings_module: str):
    from mypy import build

    old_load_graph = build.load_graph

    def patched_load_graph(sources: List[BuildSource], manager: BuildManager,
                           old_graph: Optional[Graph] = None,
                           new_modules: Optional[List[State]] = None):
        if all([source.module != settings_module for source in sources]):
            sources.append(BuildSource(None, settings_module, None))

        return old_load_graph(sources=sources, manager=manager,
                              old_graph=old_graph,
                              new_modules=new_modules)

    build.load_graph = patched_load_graph


def replace_apply_function_plugin_method():
    def apply_function_plugin(self,
                              arg_types: List[Type],
                              inferred_ret_type: Type,
                              arg_names: Optional[Sequence[Optional[str]]],
                              formal_to_actual: List[List[int]],
                              args: List[Expression],
                              num_formals: int,
                              fullname: str,
                              object_type: Optional[Type],
                              context: Context) -> Type:
        """Use special case logic to infer the return type of a specific named function/method.

        Caller must ensure that a plugin hook exists. There are two different cases:

        - If object_type is None, the caller must ensure that a function hook exists
          for fullname.
        - If object_type is not None, the caller must ensure that a method hook exists
          for fullname.

        Return the inferred return type.
        """
        formal_arg_types = [[] for _ in range(num_formals)]  # type: List[List[Type]]
        formal_arg_exprs = [[] for _ in range(num_formals)]  # type: List[List[Expression]]
        formal_arg_names = [None for _ in range(num_formals)]  # type: List[Optional[str]]
        for formal, actuals in enumerate(formal_to_actual):
            for actual in actuals:
                formal_arg_types[formal].append(arg_types[actual])
                formal_arg_exprs[formal].append(args[actual])
                if arg_names:
                    formal_arg_names[formal] = arg_names[actual]

        num_passed_positionals = sum([1 if name is None else 0
                                     for name in formal_arg_names])
        if arg_names and num_passed_positionals > 0:
            object_type_info = None
            if object_type is not None:
                if isinstance(object_type, CallableType):
                    # class object, convert to corresponding Instance
                    object_type = object_type.ret_type
                if isinstance(object_type, Instance):
                    # skip TypedDictType and others
                    object_type_info = object_type.type

            defn_arg_names = self._get_defn_arg_names(fullname, object_type=object_type_info)
            if defn_arg_names:
                if num_formals < len(defn_arg_names):
                    # self/cls argument has been passed implicitly
                    defn_arg_names = defn_arg_names[1:]
                formal_arg_names[:num_passed_positionals] = defn_arg_names[:num_passed_positionals]

        if object_type is None:
            # Apply function plugin
            callback = self.plugin.get_function_hook(fullname)
            assert callback is not None  # Assume that caller ensures this
            return callback(
                FunctionContext(formal_arg_names, formal_arg_types,
                                inferred_ret_type, formal_arg_exprs,
                                context, self.chk))
        else:
            # Apply method plugin
            method_callback = self.plugin.get_method_hook(fullname)
            assert method_callback is not None  # Assume that caller ensures this
            return method_callback(
                MethodContext(object_type, formal_arg_names, formal_arg_types,
                              inferred_ret_type, formal_arg_exprs,
                              context, self.chk))

    from mypy.checkexpr import ExpressionChecker
    ExpressionChecker.apply_function_plugin = apply_function_plugin

