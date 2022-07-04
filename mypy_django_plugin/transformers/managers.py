from typing import Optional, Union

from mypy.checker import TypeChecker, fill_typevars
from mypy.nodes import (
    GDEF,
    CallExpr,
    Decorator,
    FuncBase,
    FuncDef,
    MemberExpr,
    OverloadedFuncDef,
    RefExpr,
    StrExpr,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import AttributeContext, DynamicClassDefContext, SemanticAnalyzerPluginInterface
from mypy.types import AnyType, CallableType, Instance, ProperType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny
from typing_extensions import Final

from mypy_django_plugin.lib import fullnames, helpers

MANAGER_METHODS_RETURNING_QUERYSET: Final = frozenset(
    (
        "alias",
        "all",
        "annotate",
        "complex_filter",
        "defer",
        "difference",
        "distinct",
        "exclude",
        "extra",
        "filter",
        "intersection",
        "none",
        "only",
        "order_by",
        "prefetch_related",
        "reverse",
        "select_for_update",
        "select_related",
        "union",
        "using",
    )
)


def get_method_type_from_dynamic_manager(
    api: TypeChecker, method_name: str, manager_instance: Instance
) -> Optional[ProperType]:
    """
    Attempt to resolve a method on a manager that was built from '.from_queryset'
    """

    manager_type_info = manager_instance.type

    if (
        "django" not in manager_type_info.metadata
        or "from_queryset_manager" not in manager_type_info.metadata["django"]
    ):
        # Manager isn't dynamically added
        return None

    queryset_fullname = manager_type_info.metadata["django"]["from_queryset_manager"]
    assert isinstance(queryset_fullname, str)
    queryset_info = helpers.lookup_fully_qualified_typeinfo(api, queryset_fullname)
    assert queryset_info is not None

    def get_funcdef_type(definition: Union[FuncBase, Decorator, None]) -> Optional[ProperType]:
        # TODO: Handle @overload?
        if isinstance(definition, FuncBase) and not isinstance(definition, OverloadedFuncDef):
            return definition.type
        elif isinstance(definition, Decorator):
            return definition.func.type
        return None

    method_type = get_funcdef_type(queryset_info.get_method(method_name))
    if method_type is None:
        return None

    assert isinstance(method_type, CallableType)

    variables = method_type.variables
    ret_type = method_type.ret_type

    is_fallback_queryset = queryset_info.metadata.get("django", {}).get("any_fallback_queryset", False)

    # For methods on the manager that return a queryset we need to override the
    # return type to be the actual queryset class, not the base QuerySet that's
    # used by the typing stubs.
    if method_name in MANAGER_METHODS_RETURNING_QUERYSET:
        if not is_fallback_queryset:
            ret_type = Instance(queryset_info, manager_instance.args)
        else:
            # The fallback queryset inherits _QuerySet, which has two generics
            # instead of the one exposed on QuerySet. That means that we need
            # to add the model twice. In real code it's not possible to inherit
            # from _QuerySet, as it doesn't exist at runtime, so this fix is
            # only needed for pluign-generated querysets.
            ret_type = Instance(queryset_info, [manager_instance.args[0], manager_instance.args[0]])
        variables = []

    # Drop any 'self' argument as our manager is already initialized
    return method_type.copy_modified(
        arg_types=method_type.arg_types[1:],
        arg_kinds=method_type.arg_kinds[1:],
        arg_names=method_type.arg_names[1:],
        variables=variables,
        ret_type=ret_type,
    )


def get_method_type_from_reverse_manager(
    api: TypeChecker, method_name: str, manager_type_info: TypeInfo
) -> Optional[ProperType]:
    """
    Attempts to resolve a reverse manager's method via the '_default_manager' manager on the related model
    From Django docs:
      "By default the RelatedManager used for reverse relations is a subclass of the default manager for that model."
    Ref: https://docs.djangoproject.com/en/dev/topics/db/queries/#using-a-custom-reverse-manager
    """
    is_reverse_manager = (
        "django" in manager_type_info.metadata and "related_manager_to_model" in manager_type_info.metadata["django"]
    )
    if not is_reverse_manager:
        return None

    related_model_fullname = manager_type_info.metadata["django"]["related_manager_to_model"]
    assert isinstance(related_model_fullname, str)
    model_info = helpers.lookup_fully_qualified_typeinfo(api, related_model_fullname)
    if model_info is None:
        return None

    # We should _always_ have a '_default_manager' on a model
    assert "_default_manager" in model_info.names
    assert isinstance(model_info.names["_default_manager"].node, Var)
    manager_instance = model_info.names["_default_manager"].node.type
    return (
        get_method_type_from_dynamic_manager(api, method_name, manager_instance)
        # TODO: Can we assert on None and Instance?
        if manager_instance is not None and isinstance(manager_instance, Instance)
        else None
    )


def resolve_manager_method_from_instance(instance: Instance, method_name: str, ctx: AttributeContext) -> MypyType:

    api = helpers.get_typechecker_api(ctx)
    method_type = get_method_type_from_dynamic_manager(
        api, method_name, instance
    ) or get_method_type_from_reverse_manager(api, method_name, instance.type)

    return method_type if method_type is not None else ctx.default_attr_type


def resolve_manager_method(ctx: AttributeContext) -> MypyType:
    """
    A 'get_attribute_hook' that is intended to be invoked whenever the TypeChecker encounters
    an attribute on a class that has 'django.db.models.BaseManager' as a base.
    """
    # Skip (method) type that is currently something other than Any
    if not isinstance(ctx.default_attr_type, AnyType):
        return ctx.default_attr_type

    # (Current state is:) We wouldn't end up here when looking up a method from a custom _manager_.
    # That's why we only attempt to lookup the method for either a dynamically added or reverse manager.
    if isinstance(ctx.context, MemberExpr):
        method_name = ctx.context.name
    elif isinstance(ctx.context, CallExpr) and isinstance(ctx.context.callee, MemberExpr):
        method_name = ctx.context.callee.name
    else:
        ctx.api.fail("Unable to resolve return type of queryset/manager method", ctx.context)
        return AnyType(TypeOfAny.from_error)

    if isinstance(ctx.type, Instance):
        return resolve_manager_method_from_instance(instance=ctx.type, method_name=method_name, ctx=ctx)
    else:
        ctx.api.fail(f'Unable to resolve return type of queryset/manager method "{method_name}"', ctx.context)
        return AnyType(TypeOfAny.from_error)


def create_new_manager_class_from_from_queryset_method(ctx: DynamicClassDefContext) -> None:
    """
    Insert a new manager class node for a: '<Name> = <Manager>.from_queryset(<QuerySet>)'.
    When the assignment expression lives at module level.
    """
    semanal_api = helpers.get_semanal_api(ctx)

    # TODO: Emit an error when called in a class scope
    if semanal_api.is_class_scope():
        return

    # Don't redeclare the manager class if we've already defined it.
    manager_node = semanal_api.lookup_current_scope(ctx.name)
    if manager_node and isinstance(manager_node.node, TypeInfo):
        # This is just a deferral run where our work is already finished
        return

    new_manager_info = create_manager_info_from_from_queryset_call(ctx.api, ctx.call, ctx.name)
    if new_manager_info is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
        return

    # So that the plugin will reparameterize the manager when it is constructed inside of a Model definition
    helpers.add_new_manager_base(semanal_api, new_manager_info.fullname)


def create_manager_info_from_from_queryset_call(
    api: SemanticAnalyzerPluginInterface, call_expr: CallExpr, name: Optional[str] = None
) -> Optional[TypeInfo]:
    """
    Extract manager and queryset TypeInfo from a from_queryset call.
    """

    if (
        # Check that this is a from_queryset call on a manager subclass
        not isinstance(call_expr.callee, MemberExpr)
        or not isinstance(call_expr.callee.expr, RefExpr)
        or not isinstance(call_expr.callee.expr.node, TypeInfo)
        or not call_expr.callee.expr.node.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME)
        or not call_expr.callee.name == "from_queryset"
        # Check that the call has one or two arguments and that the first is a
        # QuerySet subclass
        or not 1 <= len(call_expr.args) <= 2
        or not isinstance(call_expr.args[0], RefExpr)
        or not isinstance(call_expr.args[0].node, TypeInfo)
        or not call_expr.args[0].node.has_base(fullnames.QUERYSET_CLASS_FULLNAME)
    ):
        return None

    base_manager_info, queryset_info = call_expr.callee.expr.node, call_expr.args[0].node
    if queryset_info.fullname is None:
        # In some cases, due to the way the semantic analyzer works, only
        # passed_queryset.name is available. But it should be analyzed again,
        # so this isn't a problem.
        return None

    if len(call_expr.args) == 2 and isinstance(call_expr.args[1], StrExpr):
        manager_name = call_expr.args[1].value
    else:
        manager_name = f"{base_manager_info.name}From{queryset_info.name}"

    new_manager_info = create_manager_class(api, base_manager_info, name or manager_name, call_expr.line)

    popuplate_manager_from_queryset(new_manager_info, queryset_info)

    manager_fullname = ".".join(["django.db.models.manager", manager_name])

    base_manager_info = new_manager_info.mro[1]
    base_manager_info.metadata.setdefault("from_queryset_managers", {})
    base_manager_info.metadata["from_queryset_managers"][manager_fullname] = new_manager_info.fullname

    # Add the new manager to the current module
    module = api.modules[api.cur_mod_id]
    module.names[name or manager_name] = SymbolTableNode(
        GDEF, new_manager_info, plugin_generated=True, no_serialize=False
    )

    return new_manager_info


def create_manager_class(
    api: SemanticAnalyzerPluginInterface, base_manager_info: TypeInfo, name: str, line: int
) -> TypeInfo:

    base_manager_instance = fill_typevars(base_manager_info)
    assert isinstance(base_manager_instance, Instance)

    manager_info = helpers.create_type_info(name, api.cur_mod_id, bases=[base_manager_instance])
    manager_info.line = line
    manager_info.type_vars = base_manager_info.type_vars
    manager_info.defn.type_vars = base_manager_info.defn.type_vars
    manager_info.defn.line = line
    manager_info.metaclass_type = manager_info.calculate_metaclass_type()

    return manager_info


def popuplate_manager_from_queryset(manager_info: TypeInfo, queryset_info: TypeInfo) -> None:
    """
    Add methods from the QuerySet class to the manager.
    """

    # Stash the queryset fullname which was passed to .from_queryset So that
    # our 'resolve_manager_method' attribute hook can fetch the method from
    # that QuerySet class
    django_metadata = helpers.get_django_metadata(manager_info)
    django_metadata["from_queryset_manager"] = queryset_info.fullname

    # We collect and mark up all methods before django.db.models.query.QuerySet as class members
    for class_mro_info in queryset_info.mro:
        if class_mro_info.fullname == fullnames.QUERYSET_CLASS_FULLNAME:
            break
        for name, sym in class_mro_info.names.items():
            if not isinstance(sym.node, (FuncDef, Decorator)):
                continue
            # Insert the queryset method name as a class member. Note that the type of
            # the method is set as Any. Figuring out the type is the job of the
            # 'resolve_manager_method' attribute hook, which comes later.
            #
            # class BaseManagerFromMyQuerySet(BaseManager):
            #    queryset_method: Any = ...
            #
            helpers.add_new_sym_for_info(
                manager_info,
                name=name,
                sym_type=AnyType(TypeOfAny.special_form),
            )

    # For methods on BaseManager that return a queryset we need to update
    # the return type to be the actual queryset subclass used. This is done
    # by adding the methods as attributes with type Any to the manager
    # class. The actual type of these methods are resolved in
    # resolve_manager_method.
    for method_name in MANAGER_METHODS_RETURNING_QUERYSET:
        helpers.add_new_sym_for_info(
            manager_info,
            name=method_name,
            sym_type=AnyType(TypeOfAny.special_form),
        )
