from typing import NamedTuple, Optional, Tuple, Union

from mypy.checker import TypeChecker
from mypy.nodes import AssignmentStmt, Expression, MemberExpr, NameExpr, RefExpr, StrExpr, TypeInfo
from mypy.plugin import FunctionContext, MethodContext
from mypy.semanal import SemanticAnalyzer
from mypy.types import Instance, ProperType, TypeVarType, UninhabitedType
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


class M2MThrough(NamedTuple):
    arg: Optional[Expression]
    model: ProperType


class M2MTo(NamedTuple):
    arg: Expression
    model: ProperType
    self: bool  # ManyToManyField('self', ...)


class M2MArguments(NamedTuple):
    to: M2MTo
    through: Optional[M2MThrough]


def fill_model_args_for_many_to_many_field(
    *,
    ctx: FunctionContext,
    model_info: TypeInfo,
    default_return_type: Instance,
    django_context: DjangoContext,
) -> Instance:
    if not ctx.args or not ctx.args[0] or len(default_return_type.args) < 2:
        return default_return_type

    args = get_m2m_arguments(ctx=ctx, model_info=model_info, django_context=django_context)
    if args is None:
        return default_return_type

    to_arg: MypyType
    if isinstance(default_return_type.args[0], UninhabitedType):
        to_arg = args.to.model
    else:
        # Avoid overwriting a decent 'to' argument
        to_arg = default_return_type.args[0]

    if isinstance(default_return_type.args[1], UninhabitedType):
        if helpers.is_abstract_model(model_info):
            # Many to many on abstract models doesn't create any implicit, concrete
            # through model, so we populate it with the upper bound to avoid error messages
            through_arg = default_return_type.type.defn.type_vars[1].upper_bound
        elif args.through is None:
            through_arg = default_return_type.args[1]
        else:
            through_arg = args.through.model
    else:
        # Avoid overwriting a decent 'through' argument
        through_arg = default_return_type.args[1]

    return default_return_type.copy_modified(args=[to_arg, through_arg])


def get_m2m_arguments(
    *,
    ctx: FunctionContext,
    model_info: TypeInfo,
    django_context: DjangoContext,
) -> Optional[M2MArguments]:
    checker = helpers.get_typechecker_api(ctx)
    to_arg = ctx.args[0][0]
    to_model: Optional[ProperType]
    if isinstance(to_arg, StrExpr) and to_arg.value == "self":
        to_model = Instance(model_info, [])
        to_self = True
    else:
        to_model = get_model_from_expression(to_arg, api=checker, django_context=django_context)
        to_self = False

    if to_model is None:
        # 'ManyToManyField()' requires the 'to' argument
        return None
    to = M2MTo(arg=to_arg, model=to_model, self=to_self)

    through = None
    if len(ctx.args) > 5 and ctx.args[5]:
        # 'ManyToManyField(..., through=)' was called
        through_arg = ctx.args[5][0]
        through_model = get_model_from_expression(through_arg, api=checker, django_context=django_context)
        if through_model is not None:
            through = M2MThrough(arg=through_arg, model=through_model)
    elif not helpers.is_abstract_model(model_info):
        # No explicit 'through' argument was provided and model is concrete. We need
        # to dig up any generated through model for this 'ManyToManyField()' field
        through_arg = None
        m2m_throughs = helpers.get_django_metadata(model_info).get("m2m_throughs", {})
        if m2m_throughs:
            field_name = None
            for defn in model_info.defn.defs.body:
                if (
                    isinstance(defn, AssignmentStmt)
                    and defn.rvalue is ctx.context
                    and len(defn.lvalues) == 1
                    and isinstance(defn.lvalues[0], NameExpr)
                ):
                    field_name = defn.lvalues[0].name
                    break

            if field_name is not None:
                through_model_fullname = m2m_throughs.get(field_name)
                if through_model_fullname is not None:
                    through_model_info = helpers.lookup_fully_qualified_typeinfo(checker, through_model_fullname)
                    if through_model_info is not None:
                        through = M2MThrough(arg=through_arg, model=Instance(through_model_info, []))

    return M2MArguments(to=to, through=through)


def get_model_from_expression(
    expr: Expression,
    *,
    api: Union[TypeChecker, SemanticAnalyzer],
    django_context: DjangoContext,
) -> Optional[ProperType]:
    """
    Attempts to resolve an expression to a 'TypeInfo' instance. Any lazy reference
    argument(e.g. "<app_label>.<object_name>") to a Django model is also attempted.
    """
    if isinstance(expr, RefExpr) and isinstance(expr.node, TypeInfo):
        if helpers.is_model_type(expr.node):
            return Instance(expr.node, [])

    lazy_reference = None
    if isinstance(expr, StrExpr):
        lazy_reference = expr.value
    elif (
        isinstance(expr, MemberExpr)
        and isinstance(expr.expr, NameExpr)
        and f"{expr.expr.fullname}.{expr.name}" == fullnames.AUTH_USER_MODEL_FULLNAME
    ):
        lazy_reference = django_context.settings.AUTH_USER_MODEL

    if lazy_reference is not None:
        model_info = helpers.resolve_lazy_reference(lazy_reference, api=api, django_context=django_context, ctx=expr)
        if model_info is not None:
            return Instance(model_info, [])
    return None


def get_related_manager_and_model(ctx: MethodContext) -> Optional[Tuple[Instance, Instance, Instance]]:
    """
    Returns a 3-tuple consisting of:
      1. A `ManyRelatedManager` instance
      2. The first type parameter (_To) instance of 1. when it's a model
      3. The second type parameter (_Through) instance of 1. when it's a model
    When encountering a `ManyRelatedManager` that has populated its 2 first type
    parameters with models. Otherwise `None` is returned.

    For example: if given a `ManyRelatedManager[A, B]` where `A` and `B` are models the
    following 3-tuple is returned: `(ManyRelatedManager[A, B], A, B)`.
    """
    if (
        isinstance(ctx.default_return_type, Instance)
        and ctx.default_return_type.type.fullname == fullnames.MANY_RELATED_MANAGER
    ):
        # This is a call to '__get__' overload with a model instance of 'ManyToManyDescriptor'.
        # Returning a 'ManyRelatedManager'. Which we want to, just like Django, build from the
        # default manager of the related model.
        many_related_manager = ctx.default_return_type
        # Require first and second type argument of 'ManyRelatedManager' to be models
        if (
            len(many_related_manager.args) >= 2
            and isinstance(many_related_manager.args[0], Instance)
            and helpers.is_model_type(many_related_manager.args[0].type)
            and isinstance(many_related_manager.args[1], Instance)
            and helpers.is_model_type(many_related_manager.args[1].type)
        ):
            return many_related_manager, many_related_manager.args[0], many_related_manager.args[1]

    return None


def refine_many_to_many_related_manager(ctx: MethodContext) -> MypyType:
    """
    Updates the 'ManyRelatedManager' returned by e.g. 'ManyToManyDescriptor' to be a subclass
    of 'ManyRelatedManager' and the related model's default manager.
    """
    related_objects = get_related_manager_and_model(ctx)
    if related_objects is None:
        return ctx.default_return_type

    many_related_manager, related_model_instance, through_model_instance = related_objects
    checker = helpers.get_typechecker_api(ctx)
    related_manager_info = helpers.get_many_to_many_manager_info(
        checker, to=related_model_instance.type, derived_from="_default_manager"
    )
    if related_manager_info is None:
        default_manager_node = related_model_instance.type.names.get("_default_manager")
        if default_manager_node is None or not isinstance(default_manager_node.type, Instance):
            return ctx.default_return_type

        # Create a reusable generic subclass that is generic over a 'through' model,
        # explicitly declared it'd could have looked something like below
        #
        # class X(models.Model): ...
        # _Through = TypeVar("_Through", bound=models.Model)
        # class X_ManyRelatedManager(ManyRelatedManager[X, _Through], type(X._default_manager), Generic[_Through]): ...
        _through_type_var = many_related_manager.type.defn.type_vars[1]
        assert isinstance(_through_type_var, TypeVarType)
        generic_to_many_related_manager = many_related_manager.copy_modified(
            args=[
                # Keep the same '_To' as the (parent) `ManyRelatedManager` instance
                many_related_manager.args[0],
                # But reset the '_Through' `TypeVar` declared for `ManyRelatedManager`
                _through_type_var.copy_modified(),
            ]
        )
        related_manager_info = helpers.add_new_class_for_module(
            module=checker.modules[related_model_instance.type.module_name],
            name=f"{related_model_instance.type.name}_ManyRelatedManager",
            bases=[generic_to_many_related_manager, default_manager_node.type],
        )
        # Reuse the '_Through' `TypeVar` from `ManyRelatedManager` in our subclass
        related_manager_info.defn.type_vars = [_through_type_var.copy_modified()]
        related_manager_info.add_type_vars()
        related_manager_info.metadata["django"] = {"related_manager_to_model": related_model_instance.type.fullname}
        # Track the existence of our manager subclass, by tying it to model it operates on
        helpers.set_many_to_many_manager_info(
            to=related_model_instance.type,
            derived_from="_default_manager",
            manager_info=related_manager_info,
        )

    return Instance(related_manager_info, [through_model_instance])
