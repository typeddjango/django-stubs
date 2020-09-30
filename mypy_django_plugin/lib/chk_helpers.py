from typing import Dict, List, Optional, Set, Union

from mypy import checker
from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    GDEF, MDEF, Block, ClassDef, Expression, MypyFile, SymbolTable, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import (
    AttributeContext, CheckerPluginInterface, FunctionContext, MethodContext,
)
from mypy.types import AnyType, Instance, TupleType
from mypy.types import Type as MypyType
from mypy.types import TypedDictType, TypeOfAny

from mypy_django_plugin.lib import helpers


def add_new_class_for_current_module(current_module: MypyFile,
                                     name: str,
                                     bases: List[Instance],
                                     fields: Optional[Dict[str, MypyType]] = None
                                     ) -> TypeInfo:
    new_class_unique_name = checker.gen_unique_name(name, current_module.names)

    # make new class expression
    classdef = ClassDef(new_class_unique_name, Block([]))
    classdef.fullname = current_module.fullname + '.' + new_class_unique_name

    # make new TypeInfo
    new_typeinfo = TypeInfo(SymbolTable(), classdef, current_module.fullname)
    new_typeinfo.bases = bases
    calculate_mro(new_typeinfo)
    new_typeinfo.calculate_metaclass_type()

    # add fields
    if fields:
        for field_name, field_type in fields.items():
            var = Var(field_name, type=field_type)
            var.info = new_typeinfo
            var._fullname = new_typeinfo.fullname + '.' + field_name
            new_typeinfo.names[field_name] = SymbolTableNode(MDEF, var, plugin_generated=True)

    classdef.info = new_typeinfo
    current_module.names[new_class_unique_name] = SymbolTableNode(GDEF, new_typeinfo, plugin_generated=True)
    return new_typeinfo


def make_oneoff_named_tuple(api: TypeChecker, name: str, fields: 'Dict[str, MypyType]') -> TupleType:
    current_module = helpers.get_current_module(api)
    namedtuple_info = add_new_class_for_current_module(current_module, name,
                                                       bases=[api.named_generic_type('typing.NamedTuple', [])],
                                                       fields=fields)
    return TupleType(list(fields.values()), fallback=Instance(namedtuple_info, []))


def make_tuple(api: 'TypeChecker', fields: List[MypyType]) -> TupleType:
    # fallback for tuples is any builtins.tuple instance
    fallback = api.named_generic_type('builtins.tuple',
                                      [AnyType(TypeOfAny.special_form)])
    return TupleType(fields, fallback=fallback)


def make_oneoff_typeddict(api: CheckerPluginInterface, fields: 'Dict[str, MypyType]',
                          required_keys: Set[str]) -> TypedDictType:
    object_type = api.named_generic_type('mypy_extensions._TypedDict', [])
    typed_dict_type = TypedDictType(fields,  # type: ignore
                                    required_keys=required_keys,
                                    fallback=object_type)
    return typed_dict_type


def get_typechecker_api(ctx: Union[AttributeContext, MethodContext, FunctionContext]) -> TypeChecker:
    if not isinstance(ctx.api, TypeChecker):
        raise ValueError('Not a TypeChecker')
    return ctx.api


def check_types_compatible(ctx: Union[FunctionContext, MethodContext],
                           *, expected_type: MypyType, actual_type: MypyType, error_message: str) -> None:
    api = get_typechecker_api(ctx)
    api.check_subtype(actual_type, expected_type,
                      ctx.context, error_message,
                      'got', 'expected')


def get_call_argument_by_name(ctx: Union[FunctionContext, MethodContext], name: str) -> Optional[Expression]:
    """
    Return the expression for the specific argument.
    This helper should only be used with non-star arguments.
    """
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    args = ctx.args[idx]
    if len(args) != 1:
        # Either an error or no value passed.
        return None
    return args[0]


def get_call_argument_type_by_name(ctx: Union[FunctionContext, MethodContext], name: str) -> Optional[MypyType]:
    """Return the type for the specific argument.

    This helper should only be used with non-star arguments.
    """
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    arg_types = ctx.arg_types[idx]
    if len(arg_types) != 1:
        # Either an error or no value passed.
        return None
    return arg_types[0]


def add_new_sym_for_info(info: TypeInfo, *, name: str, sym_type: MypyType) -> None:
    # type=: type of the variable itself
    var = Var(name=name, type=sym_type)
    # var.info: type of the object variable is bound to
    var.info = info
    var._fullname = info.fullname + '.' + name
    var.is_initialized_in_class = True
    var.is_inferred = True
    info.names[name] = SymbolTableNode(MDEF, var,
                                       plugin_generated=True)
