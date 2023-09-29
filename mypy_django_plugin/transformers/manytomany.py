from typing import NamedTuple, Optional, Union

from mypy.checker import TypeChecker
from mypy.nodes import AssignmentStmt, Expression, MemberExpr, NameExpr, StrExpr, TypeInfo
from mypy.plugin import FunctionContext
from mypy.semanal import SemanticAnalyzer
from mypy.types import Instance, ProperType, UninhabitedType
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
    if isinstance(expr, NameExpr) and isinstance(expr.node, TypeInfo):
        if (
            expr.node.metaclass_type is not None
            and expr.node.metaclass_type.type.fullname == fullnames.MODEL_METACLASS_FULLNAME
        ):
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
