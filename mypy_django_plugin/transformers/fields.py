from typing import Optional, Tuple, cast

from mypy.checker import TypeChecker
from mypy.nodes import StrExpr, TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import AnyType, CallableType, Instance, Type as MypyType, UnionType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


def extract_referred_to_type(ctx: FunctionContext, django_context: DjangoContext) -> Optional[Instance]:
    api = cast(TypeChecker, ctx.api)
    if 'to' not in ctx.callee_arg_names:
        api.msg.fail(f'to= parameter must be set for {ctx.context.callee.fullname!r}',
                     context=ctx.context)
        return None

    arg_type = ctx.arg_types[ctx.callee_arg_names.index('to')][0]
    if not isinstance(arg_type, CallableType):
        to_arg_expr = ctx.args[ctx.callee_arg_names.index('to')][0]
        if not isinstance(to_arg_expr, StrExpr):
            # not string, not supported
            return None

        model_string = to_arg_expr.value
        if model_string == 'self':
            model_fullname = api.tscope.classes[-1].fullname()
        elif '.' not in model_string:
            model_fullname = api.tscope.classes[-1].module_name + '.' + model_string
        else:
            if django_context.app_models is not None and model_string in django_context.app_models:
                model_fullname = django_context.app_models[model_string]
            else:
                ctx.api.fail(f'Cannot find referenced model for {model_string!r}', context=ctx.context)
                return None

        model_info = helpers.lookup_fully_qualified_generic(model_fullname, all_modules=api.modules)
        if model_info is None or not isinstance(model_info, TypeInfo):
            raise helpers.IncompleteDefnException(model_fullname)

        return Instance(model_info, [])

    referred_to_type = arg_type.ret_type
    assert isinstance(referred_to_type, Instance)

    if not referred_to_type.type.has_base(fullnames.MODEL_CLASS_FULLNAME):
        ctx.api.msg.fail(f'to= parameter value must be a subclass of {fullnames.MODEL_CLASS_FULLNAME!r}',
                         context=ctx.context)
        return None

    return referred_to_type


def convert_any_to_type(typ: MypyType, replacement_type: MypyType) -> MypyType:
    """
    Converts any encountered Any (in typ itself, or in generic parameters) into referred_to_type
    """
    if isinstance(typ, UnionType):
        converted_items = []
        for item in typ.items:
            converted_items.append(convert_any_to_type(item, replacement_type))
        return UnionType.make_union(converted_items,
                                    line=typ.line, column=typ.column)
    if isinstance(typ, Instance):
        args = []
        for default_arg in typ.args:
            if isinstance(default_arg, AnyType):
                args.append(replacement_type)
            else:
                args.append(default_arg)
        return helpers.reparametrize_instance(typ, args)

    if isinstance(typ, AnyType):
        return replacement_type

    return typ


def get_referred_to_model_fullname(ctx: FunctionContext, django_context: DjangoContext) -> str:
    to_arg_type = helpers.get_call_argument_type_by_name(ctx, 'to')
    if isinstance(to_arg_type, CallableType):
        assert isinstance(to_arg_type.ret_type, Instance)
        return to_arg_type.ret_type.type.fullname()

    to_arg_expr = helpers.get_call_argument_by_name(ctx, 'to')
    if not isinstance(to_arg_expr, StrExpr):
        raise helpers.IncompleteDefnException(f'Not a string: {to_arg_expr}')

    outer_model_info = ctx.api.tscope.classes[-1]
    assert isinstance(outer_model_info, TypeInfo)

    model_string = to_arg_expr.value
    if model_string == 'self':
        return outer_model_info.fullname()
    if '.' not in model_string:
        # same file class
        return outer_model_info.module_name + '.' + model_string

    model_cls = django_context.apps_registry.get_model(model_string)
    model_fullname = helpers.get_class_fullname(model_cls)
    return model_fullname


def fill_descriptor_types_for_related_field(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    referred_to_fullname = get_referred_to_model_fullname(ctx, django_context)
    referred_to_typeinfo = helpers.lookup_fully_qualified_generic(referred_to_fullname, ctx.api.modules)
    assert isinstance(referred_to_typeinfo, TypeInfo), f'Cannot resolve {referred_to_fullname!r}'
    referred_to_type = Instance(referred_to_typeinfo, [])

    default_related_field_type = set_descriptor_types_for_field(ctx)
    # replace Any with referred_to_type
    args = []
    for default_arg in default_related_field_type.args:
        args.append(convert_any_to_type(default_arg, referred_to_type))

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
        args.append(convert_any_to_type(default_arg, base_type))

    return helpers.reparametrize_instance(default_return_type, args)


# def _parse_choices_type(ctx: FunctionContext, choices_arg: Expression) -> Optional[str]:
#     if isinstance(choices_arg, (TupleExpr, ListExpr)):
#         # iterable of 2 element tuples of two kinds
#         _, analyzed_choices = ctx.api.analyze_iterable_item_type(choices_arg)
#         if isinstance(analyzed_choices, TupleType):
#             first_element_type = analyzed_choices.items[0]
#             if isinstance(first_element_type, Instance):
#                 return first_element_type.type.fullname()


# def _parse_referenced_model(ctx: FunctionContext, to_arg: Expression) -> Optional[TypeInfo]:
#     if isinstance(to_arg, NameExpr) and isinstance(to_arg.node, TypeInfo):
#         # reference to the model class
#         return to_arg.node
#
#     elif isinstance(to_arg, StrExpr):
#         referenced_model_info = helpers.get_model_info(to_arg.value, ctx.api.modules)
#         if referenced_model_info is not None:
#             return referenced_model_info


# def parse_field_init_arguments_into_model_metadata(ctx: FunctionContext) -> None:
#     outer_model = ctx.api.scope.active_class()
#     if outer_model is None or not outer_model.has_base(fullnames.MODEL_CLASS_FULLNAME):
#         # outside models.Model class, undetermined
#         return
#
#     # Determine name of the current field
#     for attr_name, stmt in helpers.iter_over_class_level_assignments(outer_model.defn):
#         if stmt == ctx.context:
#             field_name = attr_name
#             break
#     else:
#         return
#
#     model_fields_metadata = metadata.get_fields_metadata(outer_model)
#
#     # primary key
#     is_primary_key = False
#     primary_key_arg = helpers.get_call_argument_by_name(ctx, 'primary_key')
#     if primary_key_arg:
#         is_primary_key = helpers.parse_bool(primary_key_arg)
#     model_fields_metadata[field_name] = {'primary_key': is_primary_key}
#
#     # choices
#     choices_arg = helpers.get_call_argument_by_name(ctx, 'choices')
#     if choices_arg:
#         choices_type_fullname = _parse_choices_type(ctx.api, choices_arg)
#         if choices_type_fullname:
#             model_fields_metadata[field_name]['choices_type'] = choices_type_fullname
#
#     # nullability
#     null_arg = helpers.get_call_argument_by_name(ctx, 'null')
#     is_nullable = False
#     if null_arg:
#         is_nullable = helpers.parse_bool(null_arg)
#     model_fields_metadata[field_name]['null'] = is_nullable
#
#     # is_blankable
#     blank_arg = helpers.get_call_argument_by_name(ctx, 'blank')
#     is_blankable = False
#     if blank_arg:
#         is_blankable = helpers.parse_bool(blank_arg)
#     model_fields_metadata[field_name]['blank'] = is_blankable
#
#     # default
#     default_arg = helpers.get_call_argument_by_name(ctx, 'default')
#     if default_arg and not helpers.is_none_expr(default_arg):
#         model_fields_metadata[field_name]['default_specified'] = True
#
#     if helpers.has_any_of_bases(ctx.default_return_type.type, fullnames.RELATED_FIELDS_CLASSES):
#         # to
#         to_arg = helpers.get_call_argument_by_name(ctx, 'to')
#         if to_arg:
#             referenced_model = _parse_referenced_model(ctx, to_arg)
#             if referenced_model is not None:
#                 model_fields_metadata[field_name]['to'] = referenced_model.fullname()
#             else:
#                 model_fields_metadata[field_name]['to'] = to_arg.value
#                 # referenced_model = to_arg.value
#                 # raise helpers.IncompleteDefnException()
#
#             # model_fields_metadata[field_name]['to'] = referenced_model.fullname()
#             # if referenced_model is not None:
#             #     model_fields_metadata[field_name]['to'] = referenced_model.fullname()
#             # else:
#             #     assert isinstance(to_arg, StrExpr)
#             #     model_fields_metadata[field_name]['to'] = to_arg.value
#
#         # related_name
#         related_name_arg = helpers.get_call_argument_by_name(ctx, 'related_name')
#         if related_name_arg:
#             if isinstance(related_name_arg, StrExpr):
#                 model_fields_metadata[field_name]['related_name'] = related_name_arg.value
#             else:
#                 model_fields_metadata[field_name]['related_name'] = outer_model.name().lower() + '_set'
