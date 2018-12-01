from typing import Optional, List, Sequence, NamedTuple, Tuple

from mypy import checkexpr
from mypy.checkexpr import map_actuals_to_formals
from mypy.checkmember import analyze_member_access
from mypy.expandtype import freshen_function_type_vars
from mypy.messages import MessageBuilder
from mypy.nodes import Expression, Context, TypeInfo, FuncDef, Decorator, RefExpr
from mypy.plugin import CheckerPluginInterface
from mypy.subtypes import is_equivalent
from mypy.types import Type, CallableType, Instance, TypeType, Overloaded, AnyType, TypeOfAny, UnionType, TypeVarType, TupleType


class PatchedExpressionChecker(checkexpr.ExpressionChecker):
    def get_argnames_of_func_node(self, func_node: Context) -> Optional[List[str]]:
        if isinstance(func_node, FuncDef):
            return func_node.arg_names
        if isinstance(func_node, Decorator):
            return func_node.func.arg_names
        if isinstance(func_node, TypeInfo):
            # __init__ method
            init_node = func_node.get_method('__init__')
            assert isinstance(init_node, FuncDef)
            return init_node.arg_names
        return None

    def get_defn_arg_names(self, fullname: str,
                           object_type: Optional[TypeInfo]) -> Optional[List[str]]:
        if object_type is not None:
            method_name = fullname.rpartition('.')[-1]
            sym = object_type.get(method_name)
            if (sym is None or sym.node is None
                    or not isinstance(sym.node, (FuncDef, Decorator, TypeInfo))):
                # arg_names extraction is unsupported for sym.node
                return None
            return self.get_argnames_of_func_node(sym.node)

        sym = self.chk.lookup_qualified(fullname)
        if sym.node is None:
            return None
        return self.get_argnames_of_func_node(sym.node)

    def check_call(self, callee: Type, args: List[Expression],
                   arg_kinds: List[int], context: Context,
                   arg_names: Optional[Sequence[Optional[str]]] = None,
                   callable_node: Optional[Expression] = None,
                   arg_messages: Optional[MessageBuilder] = None,
                   callable_name: Optional[str] = None,
                   object_type: Optional[Type] = None) -> Tuple[Type, Type]:
        """Type check a call.

        Also infer type arguments if the callee is a generic function.

        Return (result type, inferred callee type).

        Arguments:
            callee: type of the called value
            args: actual argument expressions
            arg_kinds: contains nodes.ARG_* constant for each argument in args
                 describing whether the argument is positional, *arg, etc.
            arg_names: names of arguments (optional)
            callable_node: associate the inferred callable type to this node,
                if specified
            arg_messages: TODO
            callable_name: Fully-qualified name of the function/method to call,
                or None if unavailable (examples: 'builtins.open', 'typing.Mapping.get')
            object_type: If callable_name refers to a method, the type of the object
                on which the method is being called
        """
        arg_messages = arg_messages or self.msg
        if isinstance(callee, CallableType):
            if callable_name is None and callee.name:
                callable_name = callee.name
            if callee.is_type_obj() and isinstance(callee.ret_type, Instance):
                callable_name = callee.ret_type.type.fullname()
            if (isinstance(callable_node, RefExpr)
                and callable_node.fullname in ('enum.Enum', 'enum.IntEnum',
                                               'enum.Flag', 'enum.IntFlag')):
                # An Enum() call that failed SemanticAnalyzerPass2.check_enum_call().
                return callee.ret_type, callee

            if (callee.is_type_obj() and callee.type_object().is_abstract
                    # Exception for Type[...]
                    and not callee.from_type_type
                    and not callee.type_object().fallback_to_any):
                type = callee.type_object()
                self.msg.cannot_instantiate_abstract_class(
                    callee.type_object().name(), type.abstract_attributes,
                    context)
            elif (callee.is_type_obj() and callee.type_object().is_protocol
                  # Exception for Type[...]
                  and not callee.from_type_type):
                self.chk.fail('Cannot instantiate protocol class "{}"'
                              .format(callee.type_object().name()), context)

            formal_to_actual = map_actuals_to_formals(
                arg_kinds, arg_names,
                callee.arg_kinds, callee.arg_names,
                lambda i: self.accept(args[i]))

            if callee.is_generic():
                callee = freshen_function_type_vars(callee)
                callee = self.infer_function_type_arguments_using_context(
                    callee, context)
                callee = self.infer_function_type_arguments(
                    callee, args, arg_kinds, formal_to_actual, context)

            arg_types = self.infer_arg_types_in_context(
                callee, args, arg_kinds, formal_to_actual)

            self.check_argument_count(callee, arg_types, arg_kinds,
                                      arg_names, formal_to_actual, context, self.msg)

            self.check_argument_types(arg_types, arg_kinds, callee,
                                      formal_to_actual, context,
                                      messages=arg_messages)

            if (callee.is_type_obj() and (len(arg_types) == 1)
                    and is_equivalent(callee.ret_type, self.named_type('builtins.type'))):
                callee = callee.copy_modified(ret_type=TypeType.make_normalized(arg_types[0]))

            if callable_node:
                # Store the inferred callable type.
                self.chk.store_type(callable_node, callee)

            if (callable_name
                    and ((object_type is None and self.plugin.get_function_hook(callable_name))
                         or (object_type is not None
                             and self.plugin.get_method_hook(callable_name)))):
                ret_type = self.apply_function_plugin(
                    arg_types, callee.ret_type, arg_names, formal_to_actual,
                    args, len(callee.arg_types), callable_name, object_type, context)
                callee = callee.copy_modified(ret_type=ret_type)
            return callee.ret_type, callee
        elif isinstance(callee, Overloaded):
            arg_types = self.infer_arg_types_in_empty_context(args)
            return self.check_overload_call(callee=callee,
                                            args=args,
                                            arg_types=arg_types,
                                            arg_kinds=arg_kinds,
                                            arg_names=arg_names,
                                            callable_name=callable_name,
                                            object_type=object_type,
                                            context=context,
                                            arg_messages=arg_messages)
        elif isinstance(callee, AnyType) or not self.chk.in_checked_function():
            self.infer_arg_types_in_empty_context(args)
            if isinstance(callee, AnyType):
                return (AnyType(TypeOfAny.from_another_any, source_any=callee),
                        AnyType(TypeOfAny.from_another_any, source_any=callee))
            else:
                return AnyType(TypeOfAny.special_form), AnyType(TypeOfAny.special_form)
        elif isinstance(callee, UnionType):
            self.msg.disable_type_names += 1
            results = [self.check_call(subtype, args, arg_kinds, context, arg_names,
                                       arg_messages=arg_messages)
                       for subtype in callee.relevant_items()]
            self.msg.disable_type_names -= 1
            return (UnionType.make_simplified_union([res[0] for res in results]),
                    callee)
        elif isinstance(callee, Instance):
            call_function = analyze_member_access('__call__', callee, context,
                                                  False, False, False, self.named_type,
                                                  self.not_ready_callback, self.msg,
                                                  original_type=callee, chk=self.chk)
            return self.check_call(call_function, args, arg_kinds, context, arg_names,
                                   callable_node, arg_messages)
        elif isinstance(callee, TypeVarType):
            return self.check_call(callee.upper_bound, args, arg_kinds, context, arg_names,
                                   callable_node, arg_messages)
        elif isinstance(callee, TypeType):
            # Pass the original Type[] as context since that's where errors should go.
            item = self.analyze_type_type_callee(callee.item, callee)
            return self.check_call(item, args, arg_kinds, context, arg_names,
                                   callable_node, arg_messages)
        elif isinstance(callee, TupleType):
            return self.check_call(callee.fallback, args, arg_kinds, context,
                                   arg_names, callable_node, arg_messages, callable_name,
                                   object_type)
        else:
            return self.msg.not_callable(callee, context), AnyType(TypeOfAny.from_error)

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
        from mypy.plugin import FunctionContext, MethodContext

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

            defn_arg_names = self.get_defn_arg_names(fullname, object_type=object_type_info)
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


def replace_apply_function_plugin_method():
    from mypy import plugin

    plugin.FunctionContext = NamedTuple(
        'FunctionContext', [
            ('arg_names', Sequence[Optional[str]]),  # List of actual argument names
            ('arg_types', List[List[Type]]),  # List of actual caller types for each formal argument
            ('default_return_type', Type),  # Return type inferred from signature
            ('args', List[List[Expression]]),  # Actual expressions for each formal argument
            ('context', Context),
            ('api', CheckerPluginInterface)])

    plugin.MethodContext = NamedTuple(
        'MethodContext', [
            ('type', Type),  # Base object type for method call
            ('arg_names', Sequence[Optional[str]]),  # List of actual argument names
            ('arg_types', List[List[Type]]),
            ('default_return_type', Type),
            ('args', List[List[Expression]]),
            ('context', Context),
            ('api', CheckerPluginInterface)])

    checkexpr.ExpressionChecker = PatchedExpressionChecker
