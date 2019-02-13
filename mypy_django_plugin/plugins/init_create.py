from typing import Any, Dict, Optional, Set, cast

from mypy.checker import TypeChecker
from mypy.nodes import FuncDef, TypeInfo, Var
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import AnyType, CallableType, Instance, Type, TypeOfAny, UnionType

from mypy_django_plugin import helpers


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
        model: TypeInfo = ctx.type.args[0].type
    else:
        if isinstance(ctx.default_return_type, AnyType):
            return ctx.default_return_type
        model: TypeInfo = ctx.default_return_type.type

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


def extract_field_setter_type(tp: Instance) -> Optional[Type]:
    if not isinstance(tp, Instance):
        return None
    if tp.type.has_base(helpers.FIELD_FULLNAME):
        set_method = tp.type.get_method('__set__')
        if isinstance(set_method, FuncDef) and isinstance(set_method.type, CallableType):
            if 'value' in set_method.type.arg_names:
                set_value_type = set_method.type.arg_types[set_method.type.arg_names.index('value')]
                if isinstance(set_value_type, Instance):
                    set_value_type = helpers.fill_typevars(tp, set_value_type)
                    return set_value_type
                elif isinstance(set_value_type, UnionType):
                    items_no_typevars = []
                    for item in set_value_type.items:
                        if isinstance(item, Instance):
                            item = helpers.fill_typevars(tp, item)
                        items_no_typevars.append(item)
                    return UnionType(items_no_typevars)

        get_method = tp.type.get_method('__get__')
        if isinstance(get_method, FuncDef) and isinstance(get_method.type, CallableType):
            return get_method.type.ret_type
    # GenericForeignKey
    if tp.type.has_base(helpers.GENERIC_FOREIGN_KEY_FULLNAME):
        return AnyType(TypeOfAny.special_form)
    return None


def get_fields_metadata(model: TypeInfo) -> Dict[str, Any]:
    return model.metadata.setdefault('django', {}).setdefault('fields', {})


def extract_primary_key_type(model: TypeInfo) -> Optional[Type]:
    for field_name, props in get_fields_metadata(model).items():
        is_primary_key = props.get('primary_key', False)
        if is_primary_key:
            return extract_field_setter_type(model.names[field_name].type)
    return None


def extract_choices_type(model: TypeInfo, field_name: str) -> Optional[str]:
    field_metadata = get_fields_metadata(model).get(field_name, {})
    if 'choices' in field_metadata:
        return field_metadata['choices']
    return None


def extract_expected_types(ctx: FunctionContext, model: TypeInfo) -> Dict[str, Type]:
    expected_types: Dict[str, Type] = {}

    primary_key_type = extract_primary_key_type(model)
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
                if isinstance(sym.node.type, Instance):
                    tp = sym.node.type
                    field_type = extract_field_setter_type(tp)
                    if field_type is None:
                        continue

                    choices_type_fullname = extract_choices_type(model, name)
                    if choices_type_fullname:
                        field_type = UnionType([field_type, ctx.api.named_generic_type(choices_type_fullname, [])])

                    if tp.type.fullname() in {helpers.FOREIGN_KEY_FULLNAME, helpers.ONETOONE_FIELD_FULLNAME}:
                        ref_to_model = tp.args[0]
                        if isinstance(ref_to_model, Instance) and ref_to_model.type.has_base(helpers.MODEL_CLASS_FULLNAME):
                            primary_key_type = extract_primary_key_type(ref_to_model.type)
                            if not primary_key_type:
                                primary_key_type = AnyType(TypeOfAny.special_form)
                            expected_types[name + '_id'] = primary_key_type
                    if field_type:
                        expected_types[name] = field_type
                elif isinstance(sym.node.type, AnyType):
                    expected_types[name] = sym.node.type
    return expected_types
