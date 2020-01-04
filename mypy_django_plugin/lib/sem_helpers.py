from typing import List, NamedTuple, Optional, Tuple, Union, cast

from mypy.nodes import Argument, FuncDef, TypeInfo, Var
from mypy.plugin import ClassDefContext, DynamicClassDefContext
from mypy.plugins.common import add_method
from mypy.semanal import SemanticAnalyzer
from mypy.types import AnyType, CallableType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny


class IncompleteDefnException(Exception):
    def __init__(self, error_message: str = '') -> None:
        super().__init__(error_message)


class BoundNameNotFound(IncompleteDefnException):
    def __init__(self, fullname: str) -> None:
        super().__init__(f'No {fullname!r} found')


def get_semanal_api(ctx: Union[ClassDefContext, DynamicClassDefContext]) -> SemanticAnalyzer:
    return cast(SemanticAnalyzer, ctx.api)


def get_nested_meta_node_for_current_class(info: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = info.names.get('Meta')
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def prepare_unannotated_method_signature(method_node: FuncDef) -> Tuple[List[Argument], MypyType]:
    prepared_arguments = []
    for argument in method_node.arguments[1:]:
        argument.type_annotation = AnyType(TypeOfAny.unannotated)
        prepared_arguments.append(argument)
    return_type = AnyType(TypeOfAny.unannotated)
    return prepared_arguments, return_type


class SignatureTuple(NamedTuple):
    arguments: List[Argument]
    return_type: Optional[MypyType]
    cannot_be_bound: bool


def analyze_callable_signature(api: SemanticAnalyzer, method_node: FuncDef) -> SignatureTuple:
    method_type = method_node.type
    assert isinstance(method_type, CallableType)

    arguments = []
    unbound = False
    for arg_name, arg_type, original_argument in zip(method_type.arg_names[1:],
                                                     method_type.arg_types[1:],
                                                     method_node.arguments[1:]):
        analyzed_arg_type = api.anal_type(arg_type)
        if analyzed_arg_type is None:
            unbound = True

        var = Var(name=original_argument.variable.name,
                  type=analyzed_arg_type)
        var.set_line(original_argument.variable)

        argument = Argument(variable=var,
                            type_annotation=arg_type,
                            initializer=original_argument.initializer,
                            kind=original_argument.kind)
        argument.set_line(original_argument)
        arguments.append(argument)

    analyzed_ret_type = api.anal_type(method_type.ret_type)
    if analyzed_ret_type is None:
        unbound = True
    return SignatureTuple(arguments, analyzed_ret_type, unbound)


def copy_method_or_incomplete_defn_exception(ctx: ClassDefContext,
                                             self_type: Instance,
                                             new_method_name: str,
                                             method_node: FuncDef) -> None:
    semanal_api = get_semanal_api(ctx)

    if method_node.type is None:
        if not semanal_api.final_iteration:
            raise IncompleteDefnException(f'Unannotated method {method_node.fullname!r}')

        arguments, return_type = prepare_unannotated_method_signature(method_node)
        add_method(ctx,
                   new_method_name,
                   args=arguments,
                   return_type=return_type,
                   self_type=self_type)
        return

    assert isinstance(method_node.type, CallableType)

    # copy global SymbolTableNode objects from original class to the current node, if not present
    original_module = semanal_api.modules[method_node.info.module_name]
    for name, sym in original_module.names.items():
        if (not sym.plugin_generated
                and name not in semanal_api.cur_mod_node.names):
            semanal_api.add_imported_symbol(name, sym, context=semanal_api.cur_mod_node)

    arguments, analyzed_return_type, unbound = analyze_callable_signature(semanal_api, method_node)
    assert len(arguments) + 1 == len(method_node.arguments)
    if unbound:
        raise IncompleteDefnException(f'Signature of method {method_node.fullname!r} is not ready')

    assert analyzed_return_type is not None

    if new_method_name in ctx.cls.info.names:
        del ctx.cls.info.names[new_method_name]
    add_method(ctx,
               new_method_name,
               args=arguments,
               return_type=analyzed_return_type,
               self_type=self_type)
