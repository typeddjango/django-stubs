from typing import Iterator, Tuple, Optional

from mypy.nodes import (
    FuncDef, MemberExpr, NameExpr, RefExpr, StrExpr, TypeInfo,
    PlaceholderNode, SymbolTableNode, GDEF
)
from mypy.plugin import ClassDefContext, DynamicClassDefContext
from mypy.types import AnyType, Instance, TypeOfAny
from mypy.typevars import fill_typevars

from mypy_django_plugin.lib import fullnames, sem_helpers, helpers


def iter_all_custom_queryset_methods(derived_queryset_info: TypeInfo) -> Iterator[Tuple[str, FuncDef]]:
    for base_queryset_info in derived_queryset_info.mro:
        if base_queryset_info.fullname == fullnames.QUERYSET_CLASS_FULLNAME:
            break
        for name, sym in base_queryset_info.names.items():
            if isinstance(sym.node, FuncDef):
                yield name, sym.node


def resolve_callee_manager_info_or_exception(ctx: DynamicClassDefContext) -> Optional[TypeInfo]:
    callee = ctx.call.callee
    assert isinstance(callee, MemberExpr)
    assert isinstance(callee.expr, RefExpr)

    callee_manager_info = callee.expr.node
    if (callee_manager_info is None
            or isinstance(callee_manager_info, PlaceholderNode)):
        raise sem_helpers.IncompleteDefnException(f'Definition of base manager {callee_manager_info.fullname} '
                                                  f'is incomplete.')

    assert isinstance(callee_manager_info, TypeInfo)
    return callee_manager_info


def resolve_passed_queryset_info_or_exception(ctx: DynamicClassDefContext) -> Optional[TypeInfo]:
    api = sem_helpers.get_semanal_api(ctx)

    passed_queryset_name_expr = ctx.call.args[0]
    assert isinstance(passed_queryset_name_expr, NameExpr)

    sym = api.lookup_qualified(passed_queryset_name_expr.name, ctx=ctx.call)
    if (sym is None
            or sym.node is None
            or isinstance(sym.node, PlaceholderNode)):
        raise sem_helpers.BoundNameNotFound(passed_queryset_name_expr.fullname)

    assert isinstance(sym.node, TypeInfo)
    return sym.node


def resolve_django_manager_info_or_exception(ctx: DynamicClassDefContext) -> Optional[TypeInfo]:
    api = sem_helpers.get_semanal_api(ctx)

    sym = api.lookup_fully_qualified_or_none(fullnames.MANAGER_CLASS_FULLNAME)
    if (sym is None
            or sym.node is None
            or isinstance(sym.node, PlaceholderNode)):
        raise sem_helpers.BoundNameNotFound(fullnames.MANAGER_CLASS_FULLNAME)

    assert isinstance(sym.node, TypeInfo)
    return sym.node


def new_manager_typeinfo(ctx: DynamicClassDefContext, callee_manager_info: TypeInfo) -> TypeInfo:
    callee_manager_type = Instance(callee_manager_info, [AnyType(TypeOfAny.unannotated)])
    api = sem_helpers.get_semanal_api(ctx)

    new_manager_class_name = ctx.name
    new_manager_info = helpers.new_typeinfo(new_manager_class_name,
                                            bases=[callee_manager_type], module_name=api.cur_mod_id)
    new_manager_info.set_line(ctx.call)
    return new_manager_info


def record_new_manager_info_fullname_into_metadata(ctx: DynamicClassDefContext,
                                                   new_manager_fullname: str,
                                                   callee_manager_info: TypeInfo,
                                                   queryset_info: TypeInfo,
                                                   django_manager_info: TypeInfo) -> None:
    if len(ctx.call.args) > 1:
        expr = ctx.call.args[1]
        assert isinstance(expr, StrExpr)
        custom_manager_generated_name = expr.value
    else:
        custom_manager_generated_name = callee_manager_info.name + 'From' + queryset_info.name

    custom_manager_generated_fullname = 'django.db.models.manager' + '.' + custom_manager_generated_name

    metadata = django_manager_info.metadata.setdefault('from_queryset_managers', {})
    metadata[custom_manager_generated_fullname] = new_manager_fullname


def create_new_manager_class_from_from_queryset_method(ctx: DynamicClassDefContext) -> None:
    semanal_api = sem_helpers.get_semanal_api(ctx)
    try:
        callee_manager_info = resolve_callee_manager_info_or_exception(ctx)
        queryset_info = resolve_passed_queryset_info_or_exception(ctx)
        django_manager_info = resolve_django_manager_info_or_exception(ctx)
    except sem_helpers.IncompleteDefnException:
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
    self_type = fill_typevars(new_manager_info)
    # self_type = Instance(new_manager_info, [])

    try:
        for name, method_node in iter_all_custom_queryset_methods(queryset_info):
            sem_helpers.copy_method_or_incomplete_defn_exception(class_def_context,
                                                                 self_type,
                                                                 new_method_name=name,
                                                                 method_node=method_node)
    except sem_helpers.IncompleteDefnException:
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
