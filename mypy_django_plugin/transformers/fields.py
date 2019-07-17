from typing import Optional, Tuple, cast

from mypy.nodes import TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import AnyType, CallableType, Instance, Type as MypyType, TypeOfAny

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


def get_referred_to_model_fullname(ctx: FunctionContext, django_context: DjangoContext) -> Optional[str]:
    to_arg_type = helpers.get_call_argument_type_by_name(ctx, 'to')
    if isinstance(to_arg_type, CallableType):
        assert isinstance(to_arg_type.ret_type, Instance)
        return to_arg_type.ret_type.type.fullname()

    outer_model_info = ctx.api.tscope.classes[-1]
    assert isinstance(outer_model_info, TypeInfo)

    to_arg_expr = helpers.get_call_argument_by_name(ctx, 'to')

    model_string = helpers.resolve_string_attribute_value(to_arg_expr, ctx, django_context)
    if model_string is None:
        # unresolvable
        return None

    if model_string == 'self':
        return outer_model_info.fullname()
    if '.' not in model_string:
        # same file class
        current_module = ctx.api.tree
        if model_string not in current_module.names:
            ctx.api.fail(f'No model {model_string!r} defined in the current module', ctx.context)
            return None
        return outer_model_info.module_name + '.' + model_string

    app_label, model_name = model_string.split('.')
    if app_label not in django_context.apps_registry.app_configs:
        ctx.api.fail(f'No installed app with label {app_label!r}', ctx.context)
        return None

    try:
        model_cls = django_context.apps_registry.get_model(app_label, model_name)
    except LookupError as exc:
        # no model in app
        ctx.api.fail(exc.args[0], ctx.context)
        return None

    model_fullname = helpers.get_class_fullname(model_cls)
    return model_fullname


def fill_descriptor_types_for_related_field(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    referred_to_fullname = get_referred_to_model_fullname(ctx, django_context)
    if referred_to_fullname is None:
        return AnyType(TypeOfAny.from_error)

    referred_to_typeinfo = helpers.lookup_fully_qualified_generic(referred_to_fullname, ctx.api.modules)
    assert isinstance(referred_to_typeinfo, TypeInfo), f'Cannot resolve {referred_to_fullname!r}'

    referred_to_type = Instance(referred_to_typeinfo, [])

    default_related_field_type = set_descriptor_types_for_field(ctx)
    # replace Any with referred_to_type
    args = []
    for default_arg in default_related_field_type.args:
        args.append(helpers.convert_any_to_type(default_arg, referred_to_type))

    return helpers.reparametrize_instance(default_related_field_type, new_args=args)


def get_field_descriptor_types(field_info: TypeInfo, is_nullable: bool) -> Tuple[MypyType, MypyType]:
    set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
                                                   is_nullable=is_nullable)
    get_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_get_type',
                                                   is_nullable=is_nullable)
    return set_type, get_type


def set_descriptor_types_for_field(ctx: FunctionContext) -> Instance:
    default_return_type = cast(Instance, ctx.default_return_type)
    is_nullable = helpers.parse_bool(helpers.get_call_argument_by_name(ctx, 'null'))
    set_type, get_type = get_field_descriptor_types(default_return_type.type, is_nullable)
    return helpers.reparametrize_instance(default_return_type, [set_type, get_type])


def transform_into_proper_return_type(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = ctx.default_return_type
    assert isinstance(default_return_type, Instance)

    # bail out if we're inside migration, not supported yet
    active_class = ctx.api.scope.active_class()
    if active_class is not None:
        if active_class.has_base(fullnames.MIGRATION_CLASS_FULLNAME):
            return ctx.default_return_type

    if helpers.has_any_of_bases(default_return_type.type, fullnames.RELATED_FIELDS_CLASSES):
        return fill_descriptor_types_for_related_field(ctx, django_context)

    if default_return_type.type.has_base(fullnames.ARRAY_FIELD_FULLNAME):
        return determine_type_of_array_field(ctx, django_context)

    return set_descriptor_types_for_field(ctx)


def determine_type_of_array_field(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = set_descriptor_types_for_field(ctx)

    base_field_arg_type = helpers.get_call_argument_type_by_name(ctx, 'base_field')
    if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
        return default_return_type

    base_type = base_field_arg_type.args[1]  # extract __get__ type
    args = []
    for default_arg in default_return_type.args:
        args.append(helpers.convert_any_to_type(default_arg, base_type))

    return helpers.reparametrize_instance(default_return_type, args)
