from typing import NamedTuple, Optional, Tuple

from mypy.nodes import AssignmentStmt, NameExpr, Node, TypeInfo
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import Instance, ProperType, UninhabitedType, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


class M2MThrough(NamedTuple):
    arg: Optional[Node]
    model: ProperType


class M2MTo(NamedTuple):
    arg: Node
    model: ProperType
    self: bool  # ManyToManyField('self', ...)


class M2MArguments(NamedTuple):
    to: M2MTo
    through: Optional[M2MThrough]


def fill_model_args_for_many_to_many_field(
    *,
    ctx: FunctionContext,
    model_info: TypeInfo,
    django_context: DjangoContext,
) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if (
        not ctx.args
        or not ctx.args[0]
        or not isinstance(default_return_type, Instance)
        or len(default_return_type.args) < 2
    ):
        return ctx.default_return_type

    args = get_m2m_arguments(ctx=ctx, model_info=model_info, django_context=django_context)
    if args is None:
        return ctx.default_return_type

    default_to_arg = get_proper_type(default_return_type.args[0])
    to_arg: MypyType
    if isinstance(default_to_arg, UninhabitedType):
        to_arg = args.to.model
    else:
        # Avoid overwriting a decent 'to' argument
        to_arg = default_return_type.args[0]

    default_through_arg = get_proper_type(default_return_type.args[1])
    if isinstance(default_through_arg, UninhabitedType):
        if helpers.is_abstract_model(model_info):
            # Many to many on abstract models doesn't create any implicit, concrete
            # through model, so we populate it with the upper bound to avoid error messages
            through_arg = default_return_type.type.defn.type_vars[1].upper_bound
        elif args.through is None:
            through_arg = default_through_arg
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
                        through = M2MThrough(arg=through_arg, model=Instance(through_model_info, []))

    return M2MArguments(to=to, through=through)


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
    default_return_type = get_proper_type(ctx.default_return_type)
    if (
        isinstance(default_return_type, Instance)
        and default_return_type.type.fullname == fullnames.MANY_RELATED_MANAGER
    ):
        # This is a call to '__get__' overload with a model instance of 'ManyToManyDescriptor'.
        # Returning a 'ManyRelatedManager'. Which we want to, just like Django, build from the
        # default manager of the related model.
        many_related_manager = default_return_type
        # Require first and second type argument of 'ManyRelatedManager' to be models
        if (
            len(many_related_manager.args) >= 2
            and isinstance((_To := get_proper_type(many_related_manager.args[0])), Instance)
            and helpers.is_model_type(_To.type)
            and isinstance((_Through := get_proper_type(many_related_manager.args[1])), Instance)
            and helpers.is_model_type(_Through.type)
        ):
            return many_related_manager, _To, _Through

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
        return ctx.default_return_type
    return Instance(related_manager_info, [through_model_instance])
