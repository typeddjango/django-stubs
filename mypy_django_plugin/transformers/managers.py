from typing import Optional, Union

from mypy.checker import TypeChecker, fill_typevars
from mypy.nodes import (
    GDEF,
    CallExpr,
    Decorator,
    FuncBase,
    FuncDef,
    MemberExpr,
    NameExpr,
    OverloadedFuncDef,
    RefExpr,
    StrExpr,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import AttributeContext, ClassDefContext, DynamicClassDefContext, MethodContext
from mypy.semanal import has_placeholder
from mypy.types import AnyType, CallableType, Instance, ProperType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny
from typing_extensions import Final

from mypy_django_plugin import errorcodes
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

    def get_funcdef(definition: Union[FuncBase, Decorator, None]) -> Optional[FuncBase]:
        # TODO: Handle @overload?
        if isinstance(definition, FuncBase) and not isinstance(definition, OverloadedFuncDef):
            return definition
        elif isinstance(definition, Decorator):
            return definition.func
        return None

    method_node = get_funcdef(queryset_info.get_method(method_name))
    if method_node is None:
        return None
    method_type = method_node.type
    if method_type is None:
        # We end here most probably because of untyped definition
        return None

    assert isinstance(method_type, CallableType)
    if method_node.is_static:
        return method_type

    variables = method_type.variables
    ret_type = method_type.ret_type

    # For methods on the manager that return a queryset we need to override the
    # return type to be the actual queryset class, not the base QuerySet that's
    # used by the typing stubs.
    if method_name in MANAGER_METHODS_RETURNING_QUERYSET:
        ret_type = Instance(queryset_info, manager_instance.args)
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

    # Do not interfere with `fail_if_manager_type_created_in_model_body`:
    # stop adding new manager, if we are inside, and fall back to any
    if semanal_api.scope.classes:
        any_type = AnyType(TypeOfAny.implementation_artifact)
        info = semanal_api.lookup_fully_qualified(semanal_api.scope.current_full_target()).node
        assert isinstance(info, TypeInfo)
        helpers.add_new_sym_for_info(info=info, name=ctx.name, sym_type=any_type)
        return

    # Don't redeclare the manager class if we've already defined it.
    manager_node = semanal_api.lookup_current_scope(ctx.name)
    if manager_node and isinstance(manager_node.node, TypeInfo):
        # This is just a deferral run where our work is already finished
        return

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

    base_manager_instance = fill_typevars(base_manager_info)
    assert isinstance(base_manager_instance, Instance)
    new_manager_info = semanal_api.basic_new_typeinfo(
        ctx.name, basetype_or_fallback=base_manager_instance, line=ctx.call.line
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
    new_manager_info.type_vars = base_manager_info.type_vars
    new_manager_info.defn.type_vars = base_manager_info.defn.type_vars
    new_manager_info.defn.line = ctx.call.line
    new_manager_info.metaclass_type = new_manager_info.calculate_metaclass_type()
    # Stash the queryset fullname which was passed to .from_queryset
    # So that our 'resolve_manager_method' attribute hook can fetch the method from that QuerySet class
    new_manager_info.metadata["django"] = {"from_queryset_manager": derived_queryset_fullname}

    if len(ctx.call.args) > 1:
        expr = ctx.call.args[1]
        assert isinstance(expr, StrExpr)
        custom_manager_generated_name = expr.value
    else:
        custom_manager_generated_name = base_manager_info.name + "From" + derived_queryset_info.name

    custom_manager_generated_fullname = ".".join(["django.db.models.manager", custom_manager_generated_name])
    base_manager_info.metadata.setdefault("from_queryset_managers", {})
    base_manager_info.metadata["from_queryset_managers"][custom_manager_generated_fullname] = new_manager_info.fullname

    # So that the plugin will reparameterize the manager when it is constructed inside of a Model definition
    helpers.add_new_manager_base(semanal_api, new_manager_info.fullname)

    class_def_context = ClassDefContext(cls=new_manager_info.defn, reason=ctx.call, api=semanal_api)
    self_type = fill_typevars(new_manager_info)
    assert isinstance(self_type, Instance)

    # We collect and mark up all methods before django.db.models.query.QuerySet as class members
    for class_mro_info in derived_queryset_info.mro:
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
                new_manager_info,
                name=name,
                sym_type=AnyType(TypeOfAny.special_form),
            )

    # For methods on BaseManager that return a queryset we need to update the
    # return type to be the actual queryset subclass used. This is done by
    # adding the methods as attributes with type Any to the manager class,
    # similar to how custom queryset methods are handled above. The actual type
    # of these methods are resolved in resolve_manager_method.
    for name in MANAGER_METHODS_RETURNING_QUERYSET:
        helpers.add_new_sym_for_info(
            new_manager_info,
            name=name,
            sym_type=AnyType(TypeOfAny.special_form),
        )

    # Insert the new manager (dynamic) class
    assert semanal_api.add_symbol_table_node(ctx.name, SymbolTableNode(GDEF, new_manager_info, plugin_generated=True))


def fail_if_manager_type_created_in_model_body(ctx: MethodContext) -> MypyType:
    """
    Method hook that checks if method `<Manager>.from_queryset` is called inside a model class body.

    Doing so won't, for instance, trigger the dynamic class hook(`create_new_manager_class_from_from_queryset_method`)
    for managers.
    """
    api = helpers.get_typechecker_api(ctx)
    outer_model_info = api.scope.active_class()
    if not outer_model_info or not outer_model_info.has_base(fullnames.MODEL_CLASS_FULLNAME):
        # Not inside a model class definition
        return ctx.default_return_type

    api.fail("`.from_queryset` called from inside model class body", ctx.context, code=errorcodes.MANAGER_UNTYPED)
    return ctx.default_return_type


def reparametrize_manager_base_hook(ctx: ClassDefContext) -> None:
    """
    This hook fixes `Managers` that are missing type vars::

        class MyManager(models.Manager): ...

    is interpreted as::

        _T = TypeVar('_T', covariant=True)
        class MyManager(models.Manager[_T]): ...

    This hook **does not** affect checking stage. Parametrization with model class
    is done in other place (`querysets.determine_proper_manager_type`).
    """
    manager = ctx.api.lookup_fully_qualified_or_none(ctx.cls.fullname)
    if manager is None or manager.node is None:
        return
    assert isinstance(manager.node, TypeInfo)

    if manager.node.type_vars:
        # We've already been here
        return

    parent_manager = next(
        (base for base in manager.node.bases if base.type.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME)),
        None,
    )
    if parent_manager is None:
        return

    preserve_typevars = (
        # If args are missing, but tvars present, don't ignore: we have to reparametrize
        not parent_manager.type.type_vars
        or parent_manager.args
        and (
            not isinstance(parent_manager.args[0], AnyType) or parent_manager.args[0].type_of_any == TypeOfAny.explicit
        )
    )
    if preserve_typevars:
        return

    base_manager = ctx.api.lookup_fully_qualified_or_none(fullnames.BASE_MANAGER_CLASS_FULLNAME)
    if base_manager is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
        return
    assert isinstance(base_manager.node, TypeInfo)

    tvars = tuple(base_manager.node.defn.type_vars)
    # For some reason, we have to defer now, otherwise `defer` is called in other place
    # on final iteration (`SemanticAnalyzer.analyze_func_def`).
    if any(map(has_placeholder, tvars)):
        assert not ctx.api.final_iteration, "Too late to reparametrize"
        ctx.api.defer()

    parent_manager.args = tvars
    manager.node.type_vars = []
    manager.node.defn.type_vars = list(tvars)
    manager.node.add_type_vars()
