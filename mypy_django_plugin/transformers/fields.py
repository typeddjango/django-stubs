from typing import Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import ListExpr, NameExpr, StrExpr, TupleExpr, TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import (
    AnyType, CallableType, Instance, TupleType, Type, UnionType,
)

from mypy_django_plugin import helpers


def extract_referred_to_type(ctx: FunctionContext) -> Optional[Instance]:
    api = cast(TypeChecker, ctx.api)
    if 'to' not in ctx.callee_arg_names:
        api.msg.fail(f'to= parameter must be set for {ctx.context.callee.fullname}',
                     context=ctx.context)
        return None

    arg_type = ctx.arg_types[ctx.callee_arg_names.index('to')][0]
    if not isinstance(arg_type, CallableType):
        to_arg_expr = ctx.args[ctx.callee_arg_names.index('to')][0]
        if not isinstance(to_arg_expr, StrExpr):
            # not string, not supported
            return None
        try:
            model_fullname = helpers.get_model_fullname_from_string(to_arg_expr.value,
                                                                    all_modules=api.modules)
        except helpers.SelfReference:
            model_fullname = api.tscope.classes[-1].fullname()

        except helpers.SameFileModel as exc:
            model_fullname = api.tscope.classes[-1].module_name + '.' + exc.model_cls_name

        if model_fullname is None:
            return None
        model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                            all_modules=api.modules)
        if model_info is None or not isinstance(model_info, TypeInfo):
            return None
        return Instance(model_info, [])

    referred_to_type = arg_type.ret_type
    if not isinstance(referred_to_type, Instance):
        return None
    if not referred_to_type.type.has_base(helpers.MODEL_CLASS_FULLNAME):
        ctx.api.msg.fail(f'to= parameter value must be '
                         f'a subclass of {helpers.MODEL_CLASS_FULLNAME}',
                         context=ctx.context)
        return None

    return referred_to_type


def convert_any_to_type(typ: Type, referred_to_type: Type) -> Type:
    if isinstance(typ, UnionType):
        converted_items = []
        for item in typ.items:
            converted_items.append(convert_any_to_type(item, referred_to_type))
        return UnionType.make_union(converted_items,
                                    line=typ.line, column=typ.column)
    if isinstance(typ, Instance):
        args = []
        for default_arg in typ.args:
            if isinstance(default_arg, AnyType):
                args.append(referred_to_type)
            else:
                args.append(default_arg)
        return helpers.reparametrize_instance(typ, args)

    if isinstance(typ, AnyType):
        return referred_to_type

    return typ


def fill_descriptor_types_for_related_field(ctx: FunctionContext) -> Type:
    default_return_type = set_descriptor_types_for_field(ctx)
    referred_to_type = extract_referred_to_type(ctx)
    if referred_to_type is None:
        return default_return_type

    # replace Any with referred_to_type
    args = []
    for default_arg in default_return_type.args:
        args.append(convert_any_to_type(default_arg, referred_to_type))

    return helpers.reparametrize_instance(ctx.default_return_type, new_args=args)


def set_descriptor_types_for_field(ctx: FunctionContext) -> Instance:
    default_return_type = cast(Instance, ctx.default_return_type)
    is_nullable = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'null'))
    set_type = helpers.get_private_descriptor_type(default_return_type.type, '_pyi_private_set_type',
                                                   is_nullable=is_nullable)
    get_type = helpers.get_private_descriptor_type(default_return_type.type, '_pyi_private_get_type',
                                                   is_nullable=is_nullable)
    return helpers.reparametrize_instance(default_return_type, [set_type, get_type])


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    default_return_type = set_descriptor_types_for_field(ctx)

    base_field_arg_type = helpers.get_argument_type_by_name(ctx, 'base_field')
    if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
        return default_return_type

    base_type = base_field_arg_type.args[1]  # extract __get__ type
    args = []
    for default_arg in default_return_type.args:
        args.append(convert_any_to_type(default_arg, base_type))

    return helpers.reparametrize_instance(default_return_type, args)


def transform_into_proper_return_type(ctx: FunctionContext) -> Type:
    default_return_type = ctx.default_return_type
    if not isinstance(default_return_type, Instance):
        return default_return_type

    if helpers.has_any_of_bases(default_return_type.type, (helpers.FOREIGN_KEY_FULLNAME,
                                                           helpers.ONETOONE_FIELD_FULLNAME,
                                                           helpers.MANYTOMANY_FIELD_FULLNAME)):
        return fill_descriptor_types_for_related_field(ctx)

    if default_return_type.type.has_base(helpers.ARRAY_FIELD_FULLNAME):
        return determine_type_of_array_field(ctx)

    return set_descriptor_types_for_field(ctx)


def adjust_return_type_of_field_instantiation(ctx: FunctionContext) -> Type:
    record_field_properties_into_outer_model_class(ctx)
    return transform_into_proper_return_type(ctx)


def record_field_properties_into_outer_model_class(ctx: FunctionContext) -> None:
    api = cast(TypeChecker, ctx.api)
    outer_model = api.scope.active_class()
    if outer_model is None or not outer_model.has_base(helpers.MODEL_CLASS_FULLNAME):
        # outside models.Model class, undetermined
        return

    field_name = None
    for name_expr, stmt in helpers.iter_over_assignments(outer_model.defn):
        if stmt == ctx.context and isinstance(name_expr, NameExpr):
            field_name = name_expr.name
            break
    if field_name is None:
        return

    fields_metadata = outer_model.metadata.setdefault('django', {}).setdefault('fields', {})

    # primary key
    is_primary_key = False
    primary_key_arg = helpers.get_argument_by_name(ctx, 'primary_key')
    if primary_key_arg:
        is_primary_key = helpers.parse_bool(primary_key_arg)
    fields_metadata[field_name] = {'primary_key': is_primary_key}

    # choices
    choices_arg = helpers.get_argument_by_name(ctx, 'choices')
    if choices_arg and isinstance(choices_arg, (TupleExpr, ListExpr)):
        # iterable of 2 element tuples of two kinds
        _, analyzed_choices = api.analyze_iterable_item_type(choices_arg)
        if isinstance(analyzed_choices, TupleType):
            first_element_type = analyzed_choices.items[0]
            if isinstance(first_element_type, Instance):
                fields_metadata[field_name]['choices'] = first_element_type.type.fullname()

    # nullability
    null_arg = helpers.get_argument_by_name(ctx, 'null')
    is_nullable = False
    if null_arg:
        is_nullable = helpers.parse_bool(null_arg)
    fields_metadata[field_name]['null'] = is_nullable

    # is_blankable
    blank_arg = helpers.get_argument_by_name(ctx, 'blank')
    is_blankable = False
    if blank_arg:
        is_blankable = helpers.parse_bool(blank_arg)
    fields_metadata[field_name]['blank'] = is_blankable

    # default
    default_arg = helpers.get_argument_by_name(ctx, 'default')
    if default_arg and not helpers.is_none_expr(default_arg):
        fields_metadata[field_name]['default_specified'] = True
