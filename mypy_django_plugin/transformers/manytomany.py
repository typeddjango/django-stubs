from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from mypy.nodes import AssignmentStmt, NameExpr, Node, TypeInfo
from mypy.types import AnyType, Instance, ProperType, UninhabitedType, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import helpers

if TYPE_CHECKING:
    from mypy.plugin import FunctionContext

    from mypy_django_plugin.django.context import DjangoContext


class M2MThrough(NamedTuple):
    arg: Node | None
    model: ProperType


class M2MTo(NamedTuple):
    arg: Node
    model: ProperType
    self: bool  # ManyToManyField('self', ...)


class M2MArguments(NamedTuple):
    to: M2MTo
    through: M2MThrough | None


def _through_arg_is_unset(m2m_field: Instance) -> bool:
    """Whether the 'through' type argument was left unsolved, or fell back on its 'Any' default."""
    if len(m2m_field.args) < 2:
        return False
    through_arg = get_proper_type(m2m_field.args[1])
    return isinstance(through_arg, (UninhabitedType, AnyType))


def fill_model_args_for_many_to_many_field(
    *,
    ctx: FunctionContext,
    model_info: TypeInfo,
    django_context: DjangoContext,
) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if not (
        ctx.args
        and ctx.args[0]
        and isinstance(default_return_type, Instance)
        and len(default_return_type.args) >= 2
        and (args := get_m2m_arguments(ctx=ctx, model_info=model_info, django_context=django_context))
    ):
        return ctx.default_return_type

    default_to_arg = get_proper_type(default_return_type.args[0])
    to_arg: MypyType
    if isinstance(default_to_arg, UninhabitedType):
        to_arg = args.to.model
    else:
        # Avoid overwriting a decent 'to' argument
        to_arg = default_return_type.args[0]

    if _through_arg_is_unset(default_return_type):
        if helpers.is_abstract_model(model_info):
            # Many to many on abstract models doesn't create any implicit, concrete
            # through model, so we populate it with the upper bound to avoid error messages
            through_arg = default_return_type.type.defn.type_vars[1].upper_bound
        elif args.through is None:
            through_arg = UninhabitedType()
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
) -> M2MArguments | None:
    checker = helpers.get_typechecker_api(ctx)
    to_arg = ctx.args[0][0]
    to_model = helpers.get_model_from_expression(
        to_arg, self_model=model_info, api=checker, django_context=django_context
    )
    if to_model is None:
        # 'ManyToManyField()' requires the 'to' argument
        return None
    to = M2MTo(arg=to_arg, model=to_model, self=to_model.type == model_info)

    through = None
    if len(ctx.args) > 5 and ctx.args[5]:
        # 'ManyToManyField(..., through=)' was called
        through_arg = ctx.args[5][0]
        through_model = helpers.get_model_from_expression(
            through_arg, self_model=model_info, api=checker, django_context=django_context
        )
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
                        through = M2MThrough(arg=through_arg, model=helpers.model_instance(through_model_info))

    return M2MArguments(to=to, through=through)
