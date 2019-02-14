from typing import Dict, Optional, Set, cast

from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo, Var
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import AnyType, Instance, Type, TypeOfAny, UnionType

from mypy_django_plugin import helpers
from mypy_django_plugin.helpers import extract_field_setter_type, extract_primary_key_type_for_set, get_fields_metadata


def extract_base_pointer_args(model: TypeInfo) -> Set[str]:
    pointer_args: Set[str] = set()
    for base in model.bases:
        if base.type.has_base(helpers.MODEL_CLASS_FULLNAME):
            parent_name = base.type.name().lower()
            pointer_args.add(f'{parent_name}_ptr')
            pointer_args.add(f'{parent_name}_ptr_id')
    return pointer_args


def redefine_and_typecheck_model_init(ctx: FunctionContext) -> Type:
    assert isinstance(ctx.default_return_type, Instance)

    api = cast(TypeChecker, ctx.api)
    model: TypeInfo = ctx.default_return_type.type

    expected_types = extract_expected_types(ctx, model)
    # order is preserved, can use for positionals
    positional_names = list(expected_types.keys())
    positional_names.remove('pk')
    visited_positionals = set()

    # check positionals
    for i, (_, actual_pos_type) in enumerate(zip(ctx.arg_names[0], ctx.arg_types[0])):
        actual_pos_name = positional_names[i]
        api.check_subtype(actual_pos_type, expected_types[actual_pos_name],
                          ctx.context,
                          'Incompatible type for "{}" of "{}"'.format(actual_pos_name,
                                                                      model.name()),
                          'got', 'expected')
        visited_positionals.add(actual_pos_name)

    # extract name of base models for _ptr
    base_pointer_args = extract_base_pointer_args(model)

    # check kwargs
    for i, (actual_name, actual_type) in enumerate(zip(ctx.arg_names[1], ctx.arg_types[1])):
        if actual_name in base_pointer_args:
            # parent_ptr args are not supported
            continue
        if actual_name in visited_positionals:
            continue
        if actual_name is None:
            # unpacked dict as kwargs is not supported
            continue
        if actual_name not in expected_types:
            ctx.api.fail('Unexpected attribute "{}" for model "{}"'.format(actual_name,
                                                                           model.name()),
                         ctx.context)
            continue
        api.check_subtype(actual_type, expected_types[actual_name],
                          ctx.context,
                          'Incompatible type for "{}" of "{}"'.format(actual_name,
                                                                      model.name()),
                          'got', 'expected')
    return ctx.default_return_type


def redefine_and_typecheck_model_create(ctx: MethodContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    if isinstance(ctx.type, Instance) and len(ctx.type.args) > 0:
        model_generic_arg = ctx.type.args[0]
    else:
        model_generic_arg = ctx.default_return_type

    if isinstance(model_generic_arg, AnyType):
        return ctx.default_return_type

    model: TypeInfo = model_generic_arg.type

    # extract name of base models for _ptr
    base_pointer_args = extract_base_pointer_args(model)
    expected_types = extract_expected_types(ctx, model)

    for actual_name, actual_type in zip(ctx.arg_names[0], ctx.arg_types[0]):
        if actual_name in base_pointer_args:
            # parent_ptr args are not supported
            continue
        if actual_name is None:
            # unpacked dict as kwargs is not supported
            continue
        if actual_name not in expected_types:
            api.fail('Unexpected attribute "{}" for model "{}"'.format(actual_name,
                                                                       model.name()),
                     ctx.context)
            continue
        api.check_subtype(actual_type, expected_types[actual_name],
                          ctx.context,
                          'Incompatible type for "{}" of "{}"'.format(actual_name,
                                                                      model.name()),
                          'got', 'expected')

    return ctx.default_return_type


def extract_choices_type(model: TypeInfo, field_name: str) -> Optional[str]:
    field_metadata = get_fields_metadata(model).get(field_name, {})
    if 'choices' in field_metadata:
        return field_metadata['choices']
    return None


def extract_expected_types(ctx: FunctionContext, model: TypeInfo) -> Dict[str, Type]:
    expected_types: Dict[str, Type] = {}

    primary_key_type = extract_primary_key_type_for_set(model)
    if not primary_key_type:
        # no explicit primary key, set pk to Any and add id
        primary_key_type = AnyType(TypeOfAny.special_form)
        expected_types['id'] = ctx.api.named_generic_type('builtins.int', [])

    expected_types['pk'] = primary_key_type
    for base in model.mro:
        for name, sym in base.names.items():
            # do not redefine special attrs
            if name in {'_meta', 'pk'}:
                continue
            if isinstance(sym.node, Var):
                if sym.node.type is None or isinstance(sym.node.type, AnyType):
                    # types are not ready, fallback to Any
                    expected_types[name] = AnyType(TypeOfAny.from_unimported_type)
                    expected_types[name + '_id'] = AnyType(TypeOfAny.from_unimported_type)

                elif isinstance(sym.node.type, Instance):
                    tp = sym.node.type
                    field_type = extract_field_setter_type(tp)
                    if field_type is None:
                        continue

                    if tp.type.fullname() in {helpers.FOREIGN_KEY_FULLNAME, helpers.ONETOONE_FIELD_FULLNAME}:
                        ref_to_model = tp.args[0]
                        primary_key_type = AnyType(TypeOfAny.special_form)
                        if isinstance(ref_to_model, Instance) and ref_to_model.type.has_base(helpers.MODEL_CLASS_FULLNAME):
                            typ = extract_primary_key_type_for_set(ref_to_model.type)
                            if typ:
                                primary_key_type = typ
                        expected_types[name + '_id'] = primary_key_type
                    if field_type:
                        expected_types[name] = field_type

    return expected_types
