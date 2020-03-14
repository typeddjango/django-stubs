from typing import Any, Dict, Iterator, Optional, Tuple

from mypy.checker import gen_unique_name
from mypy.nodes import (
    GDEF, CallExpr, Context, Decorator, FuncDef, MemberExpr, NameExpr, OverloadedFuncDef, PlaceholderNode, RefExpr,
    StrExpr, SymbolTable, SymbolTableNode, TypeInfo,
    MypyFile)
from mypy.plugin import ClassDefContext, DynamicClassDefContext, MethodContext
from mypy.semanal import SemanticAnalyzer, is_same_symbol, is_valid_replacement
from mypy.types import AnyType, CallableType, Instance, TypeVarType, TypeVarDef
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import chk_helpers, fullnames, helpers, sem_helpers


def iter_all_custom_queryset_methods(derived_queryset_info: TypeInfo) -> Iterator[Tuple[str, FuncDef]]:
    for base_queryset_info in derived_queryset_info.mro:
        if base_queryset_info.fullname == fullnames.QUERYSET_CLASS_FULLNAME:
            break
        for name, sym in base_queryset_info.names.items():
            if isinstance(sym.node, FuncDef):
                yield name, sym.node


def generate_from_queryset_name(base_manager_info: TypeInfo, queryset_info: TypeInfo) -> str:
    return base_manager_info.name + 'From' + queryset_info.name


#
# def cb_resolve_callee_info_or_exception(cb: ) -> TypeInfo:
#     callee = ctx.call.callee
#     assert isinstance(callee, MemberExpr)
#     assert isinstance(callee.expr, RefExpr)
#
#     callee_info = callee.expr.node
#     if (callee_info is None
#             or isinstance(callee_info, PlaceholderNode)):
#         raise sem_helpers.IncompleteDefnError(f'Definition of base manager {callee.fullname!r} '
#                                                   f'is incomplete.')
#
#     assert isinstance(callee_info, TypeInfo)
#     return callee_info


def resolve_callee_info_or_exception(callback: helpers.DynamicClassPluginCallback) -> TypeInfo:
    callee = callback.call_expr.callee
    assert isinstance(callee, MemberExpr)
    assert isinstance(callee.expr, RefExpr)

    callee_info = callee.expr.node
    if (callee_info is None
            or isinstance(callee_info, PlaceholderNode)):
        raise sem_helpers.IncompleteDefnError(f'Definition of base manager {callee.fullname!r} '
                                              f'is incomplete.')

    assert isinstance(callee_info, TypeInfo)
    return callee_info


def resolve_passed_queryset_info_or_exception(callback: helpers.DynamicClassPluginCallback) -> TypeInfo:
    passed_queryset_name_expr = callback.call_expr.args[0]
    assert isinstance(passed_queryset_name_expr, NameExpr)

    # lookup in the same module
    sym = callback.semanal_api.lookup_qualified(passed_queryset_name_expr.name, ctx=callback.call_expr)
    if (sym is None
            or sym.node is None
            or isinstance(sym.node, PlaceholderNode)):
        bound_name = passed_queryset_name_expr.fullname or passed_queryset_name_expr.name
        raise sem_helpers.BoundNameNotFound(bound_name)

    assert isinstance(sym.node, TypeInfo)
    return sym.node


def resolve_django_manager_info_or_exception(callback: helpers.DynamicClassPluginCallback) -> TypeInfo:
    info = callback.lookup_typeinfo_or_defer(fullnames.MANAGER_CLASS_FULLNAME)
    if info is None:
        raise sem_helpers.BoundNameNotFound(fullnames.MANAGER_CLASS_FULLNAME)

    return info


def new_manager_typeinfo(ctx: DynamicClassDefContext, callee_manager_info: TypeInfo) -> TypeInfo:
    callee_manager_type = Instance(callee_manager_info, [AnyType(TypeOfAny.unannotated)])
    api = sem_helpers.get_semanal_api(ctx)

    new_manager_class_name = ctx.name
    new_manager_info = helpers.new_typeinfo(new_manager_class_name,
                                            bases=[callee_manager_type], module_name=api.cur_mod_id)
    new_manager_info.set_line(ctx.call)
    return new_manager_info


def get_generated_manager_fullname(call: CallExpr, base_manager_info: TypeInfo, queryset_info: TypeInfo) -> str:
    if len(call.args) > 1:
        # only for from_queryset()
        expr = call.args[1]
        assert isinstance(expr, StrExpr)
        custom_manager_generated_name = expr.value
    else:
        custom_manager_generated_name = base_manager_info.name + 'From' + queryset_info.name

    custom_manager_generated_fullname = 'django.db.models.manager' + '.' + custom_manager_generated_name
    return custom_manager_generated_fullname


def get_generated_managers_metadata(django_manager_info: TypeInfo) -> Dict[str, Any]:
    return django_manager_info.metadata.setdefault('from_queryset_managers', {})


def record_new_manager_info_fullname_into_metadata(ctx: DynamicClassDefContext,
                                                   new_manager_fullname: str,
                                                   callee_manager_info: TypeInfo,
                                                   queryset_info: TypeInfo,
                                                   django_manager_info: TypeInfo) -> None:
    custom_manager_generated_fullname = get_generated_manager_fullname(ctx.call,
                                                                       base_manager_info=callee_manager_info,
                                                                       queryset_info=queryset_info)
    metadata = get_generated_managers_metadata(django_manager_info)
    metadata[custom_manager_generated_fullname] = new_manager_fullname


def create_new_manager_class_from_from_queryset_method(ctx: DynamicClassDefContext) -> None:
    semanal_api = sem_helpers.get_semanal_api(ctx)
    try:
        callee_manager_info = resolve_callee_info_or_exception(ctx)
        queryset_info = resolve_passed_queryset_info_or_exception(ctx)
        django_manager_info = resolve_django_manager_info_or_exception(ctx)
    except sem_helpers.IncompleteDefnError:
        if not semanal_api.final_iteration:
            semanal_api.defer()
            return
        else:
            raise

    new_manager_info = new_manager_typeinfo(ctx, callee_manager_info)
    record_new_manager_info_fullname_into_metadata(ctx,
                                                   new_manager_info.fullname,
                                                   callee_manager_info,
                                                   queryset_info,
                                                   django_manager_info)

    class_def_context = ClassDefContext(cls=new_manager_info.defn,
                                        reason=ctx.call, api=semanal_api)
    self_type = Instance(new_manager_info, [AnyType(TypeOfAny.explicit)])

    try:
        for name, method_node in iter_all_custom_queryset_methods(queryset_info):
            sem_helpers.copy_method_or_incomplete_defn_exception(class_def_context,
                                                                 self_type,
                                                                 new_method_name=name,
                                                                 method_node=method_node)
    except sem_helpers.IncompleteDefnError:
        if not semanal_api.final_iteration:
            semanal_api.defer()
            return
        else:
            raise

    new_manager_sym = SymbolTableNode(GDEF, new_manager_info, plugin_generated=True)

    # context=None - forcibly replace old node
    added = semanal_api.add_symbol_table_node(ctx.name, new_manager_sym, context=None)
    if added:
        # replace all references to the old manager Var everywhere
        for _, module in semanal_api.modules.items():
            if module.fullname != semanal_api.cur_mod_id:
                for sym_name, sym in module.names.items():
                    if sym.fullname == new_manager_info.fullname:
                        module.names[sym_name] = new_manager_sym.copy()

    # we need another iteration to process methods
    if (not added
            and not semanal_api.final_iteration):
        semanal_api.defer()


def add_symbol_table_node(api: SemanticAnalyzer,
                          name: str,
                          symbol: SymbolTableNode,
                          context: Optional[Context] = None,
                          symbol_table: Optional[SymbolTable] = None,
                          can_defer: bool = True,
                          escape_comprehensions: bool = False) -> bool:
    """Add symbol table node to the currently active symbol table.

    Return True if we actually added the symbol, or False if we refused
    to do so (because something is not ready or it was a no-op).

    Generate an error if there is an invalid redefinition.

    If context is None, unconditionally add node, since we can't report
    an error. Note that this is used by plugins to forcibly replace nodes!

    TODO: Prevent plugins from replacing nodes, as it could cause problems?

    Args:
        name: short name of symbol
        symbol: Node to add
        can_defer: if True, defer current target if adding a placeholder
        context: error context (see above about None value)
    """
    names = symbol_table or api.current_symbol_table(escape_comprehensions=escape_comprehensions)
    existing = names.get(name)
    if isinstance(symbol.node, PlaceholderNode) and can_defer:
        api.defer(context)
    if (existing is not None
            and context is not None
            and not is_valid_replacement(existing, symbol)):
        # There is an existing node, so this may be a redefinition.
        # If the new node points to the same node as the old one,
        # or if both old and new nodes are placeholders, we don't
        # need to do anything.
        old = existing.node
        new = symbol.node
        if isinstance(new, PlaceholderNode):
            # We don't know whether this is okay. Let's wait until the next iteration.
            return False
        if not is_same_symbol(old, new):
            if isinstance(new, (FuncDef, Decorator, OverloadedFuncDef, TypeInfo)):
                api.add_redefinition(names, name, symbol)
            if not (isinstance(new, (FuncDef, Decorator))
                    and api.set_original_def(old, new)):
                api.name_already_defined(name, context, existing)
    elif name not in api.missing_names and '*' not in api.missing_names:
        names[name] = symbol
        api.progress = True
        return True
    return False

