from mypy.nodes import GDEF, Decorator, FuncDef, MemberExpr, NameExpr, RefExpr, StrExpr, SymbolTableNode, TypeInfo
from mypy.plugin import ClassDefContext, DynamicClassDefContext
from mypy.types import AnyType, Instance, TypeOfAny, get_proper_type

from mypy_django_plugin.lib import fullnames, helpers


def create_new_manager_class_from_from_queryset_method(ctx: DynamicClassDefContext) -> None:
    semanal_api = helpers.get_semanal_api(ctx)

    callee = ctx.call.callee
    assert isinstance(callee, MemberExpr)
    assert isinstance(callee.expr, RefExpr)

    base_manager_info = callee.expr.node
    if base_manager_info is None:
        if not semanal_api.final_iteration:
            semanal_api.defer()
        return

    assert isinstance(base_manager_info, TypeInfo)

    passed_queryset = ctx.call.args[0]
    assert isinstance(passed_queryset, NameExpr)

    derived_queryset_fullname = passed_queryset.fullname
    if derived_queryset_fullname is None:
        # In some cases, due to the way the semantic analyzer works, only passed_queryset.name is available.
        # But it should be analyzed again, so this isn't a problem.
        return

    new_manager_info = semanal_api.basic_new_typeinfo(
        ctx.name, basetype_or_fallback=Instance(base_manager_info, [AnyType(TypeOfAny.unannotated)]), line=ctx.call.line
    )

    sym = semanal_api.lookup_fully_qualified_or_none(derived_queryset_fullname)
    assert sym is not None
    if sym.node is None:
        if not semanal_api.final_iteration:
            semanal_api.defer()
        else:
            # inherit from Any to prevent false-positives, if queryset class cannot be resolved
            new_manager_info.fallback_to_any = True
        return

    derived_queryset_info = sym.node
    assert isinstance(derived_queryset_info, TypeInfo)

    new_manager_info.line = ctx.call.line
    new_manager_info.defn.line = ctx.call.line
    # new_manager_info.bases.append(Instance(derived_queryset_info, [AnyType(TypeOfAny.unannotated)]))
    new_manager_info.metaclass_type = new_manager_info.calculate_metaclass_type()

    current_module = semanal_api.cur_mod_node
    current_module.names[ctx.name] = SymbolTableNode(GDEF, new_manager_info, plugin_generated=True)

    if len(ctx.call.args) > 1:
        expr = ctx.call.args[1]
        assert isinstance(expr, StrExpr)
        custom_manager_generated_name = expr.value
    else:
        custom_manager_generated_name = base_manager_info.name + "From" + derived_queryset_info.name

    custom_manager_generated_fullname = ".".join(["django.db.models.manager", custom_manager_generated_name])
    if "from_queryset_managers" not in base_manager_info.metadata:
        base_manager_info.metadata["from_queryset_managers"] = {}
    base_manager_info.metadata["from_queryset_managers"][custom_manager_generated_fullname] = new_manager_info.fullname

    class_def_context = ClassDefContext(cls=new_manager_info.defn, reason=ctx.call, api=semanal_api)
    self_type = Instance(new_manager_info, [])

    queryset_method_names = []

    # we need to copy all methods in MRO before django.db.models.query.QuerySet
    for class_mro_info in derived_queryset_info.mro:
        if class_mro_info.fullname == fullnames.QUERYSET_CLASS_FULLNAME:
            for name, sym in class_mro_info.names.items():
                queryset_method_names.append(name)
            break
        for name, sym in class_mro_info.names.items():
            if isinstance(sym.node, FuncDef):
                func_node = sym.node
            elif isinstance(sym.node, Decorator):
                func_node = sym.node.func
            else:
                continue
            helpers.copy_method_to_another_class(
                class_def_context, self_type, new_method_name=name, method_node=func_node
            )

    # Copy/alter all methods in common between BaseManager/QuerySet over to the new manager if their return type is
    # QuerySet. Alter the return type to be the custom queryset.
    for manager_mro_info in new_manager_info.mro:
        if manager_mro_info.fullname != fullnames.BASE_MANAGER_CLASS_FULLNAME:
            continue

        for name, sym in manager_mro_info.names.items():
            if name not in queryset_method_names:
                continue

            if isinstance(sym.node, FuncDef):
                func_node = sym.node
            elif isinstance(sym.node, Decorator):
                func_node = sym.node.func
            else:
                continue
            bound_return_type = helpers.get_method_return_type(semanal_api, func_node)
            if bound_return_type is None:
                continue

            bound_return_type = get_proper_type(bound_return_type)
            if not isinstance(bound_return_type, Instance):
                continue
            if not bound_return_type.type.has_base(fullnames.QUERYSET_CLASS_FULLNAME):
                continue

            return_type = Instance(derived_queryset_info, bound_return_type.args)

            helpers.copy_method_to_another_class(
                class_def_context,
                self_type,
                new_method_name=name,
                method_node=func_node,
                override_return_type=return_type,
            )
