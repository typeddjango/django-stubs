import typing
from typing import Dict, Optional

from mypy.nodes import Expression, FuncDef, ImportedName, MypyFile, NameExpr, SymbolNode, TypeInfo, Var
from mypy.plugin import FunctionContext
from mypy.types import AnyType, CallableType, Instance, Type, TypeOfAny, TypeVarType

MODEL_CLASS_FULLNAME = 'django.db.models.base.Model'
FIELD_FULLNAME = 'django.db.models.fields.Field'
GENERIC_FOREIGN_KEY_FULLNAME = 'django.contrib.contenttypes.fields.GenericForeignKey'
FOREIGN_KEY_FULLNAME = 'django.db.models.fields.related.ForeignKey'
ONETOONE_FIELD_FULLNAME = 'django.db.models.fields.related.OneToOneField'
MANYTOMANY_FIELD_FULLNAME = 'django.db.models.fields.related.ManyToManyField'
DUMMY_SETTINGS_BASE_CLASS = 'django.conf._DjangoConfLazyObject'

QUERYSET_CLASS_FULLNAME = 'django.db.models.query.QuerySet'
BASE_MANAGER_CLASS_FULLNAME = 'django.db.models.manager.BaseManager'
MANAGER_CLASS_FULLNAME = 'django.db.models.manager.Manager'
RELATED_MANAGER_CLASS_FULLNAME = 'django.db.models.manager.RelatedManager'

MANAGER_CLASSES = {
    MANAGER_CLASS_FULLNAME,
    RELATED_MANAGER_CLASS_FULLNAME,
    BASE_MANAGER_CLASS_FULLNAME,
    QUERYSET_CLASS_FULLNAME
}


def get_models_file(app_name: str, all_modules: typing.Dict[str, MypyFile]) -> Optional[MypyFile]:
    models_module = '.'.join([app_name, 'models'])
    return all_modules.get(models_module)


def get_model_fullname(app_name: str, model_name: str,
                       all_modules: Dict[str, MypyFile]) -> Optional[str]:
    models_file = get_models_file(app_name, all_modules)
    if models_file is None:
        # not imported so far, not supported
        return None
    sym = models_file.names.get(model_name)
    if not sym:
        return None

    if isinstance(sym.node, TypeInfo):
        return sym.node.fullname()
    elif isinstance(sym.node, ImportedName):
        return sym.node.target_fullname
    else:
        return None


class InvalidModelString(ValueError):
    def __init__(self, model_string: str):
        self.model_string = model_string


class SelfReference(ValueError):
    pass


def get_model_fullname_from_string(model_string: str,
                                   all_modules: Dict[str, MypyFile]) -> Optional[str]:
    if model_string == 'self':
        raise SelfReference()

    if '.' not in model_string:
        raise InvalidModelString(model_string)

    app_name, model_name = model_string.split('.')
    return get_model_fullname(app_name, model_name, all_modules)


def lookup_fully_qualified_generic(name: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolNode]:
    if '.' not in name:
        return None
    module, cls_name = name.rsplit('.', 1)

    module_file = all_modules.get(module)
    if module_file is None:
        return None
    sym = module_file.names.get(cls_name)
    if sym is None:
        return None
    return sym.node


def parse_bool(expr: Expression) -> Optional[bool]:
    if isinstance(expr, NameExpr):
        if expr.fullname == 'builtins.True':
            return True
        if expr.fullname == 'builtins.False':
            return False
    return None


def reparametrize_with(instance: Instance, new_typevars: typing.List[Type]):
    return Instance(instance.type, args=new_typevars)


def fill_typevars_with_any(instance: Instance) -> Type:
    return reparametrize_with(instance, [AnyType(TypeOfAny.unannotated)])


def extract_typevar_value(tp: Instance, typevar_name: str):
    return tp.args[tp.type.type_vars.index(typevar_name)]


def extract_field_setter_type(tp: Instance) -> Optional[Type]:
    if tp.type.has_base(FIELD_FULLNAME):
        set_method = tp.type.get_method('__set__')
        if isinstance(set_method, FuncDef) and isinstance(set_method.type, CallableType):
            if 'value' in set_method.type.arg_names:
                set_value_type = set_method.type.arg_types[set_method.type.arg_names.index('value')]
                if isinstance(set_value_type, Instance):
                    typevar_values: typing.List[Type] = []
                    for typevar_arg in set_value_type.args:
                        if isinstance(typevar_arg, TypeVarType):
                            typevar_values.append(extract_typevar_value(tp, typevar_arg.name))
                        # if there are typevars, extract from
                    set_value_type = reparametrize_with(set_value_type, typevar_values)
                    return set_value_type

        get_method = tp.type.get_method('__get__')
        if isinstance(get_method, FuncDef) and isinstance(get_method.type, CallableType):
            return get_method.type.ret_type
    # GenericForeignKey
    if tp.type.has_base(GENERIC_FOREIGN_KEY_FULLNAME):
        return AnyType(TypeOfAny.special_form)
    return None


def extract_primary_key_type(model: TypeInfo) -> Optional[Type]:
    # only primary keys defined in current class for now
    for sym in model.names.values():
        if isinstance(sym.node, Var) and isinstance(sym.node.type, Instance):
            tp = sym.node.type
            if tp.type.metadata.get('django', {}).get('defined_as_primary_key'):
                field_type = extract_field_setter_type(tp)
                return field_type
    return None


def extract_expected_types(ctx: FunctionContext, model: TypeInfo) -> Dict[str, Type]:
    expected_types: Dict[str, Type] = {}
    for base in model.mro:
        for name, sym in base.names.items():
            if isinstance(sym.node, Var) and isinstance(sym.node.type, Instance):
                tp = sym.node.type
                field_type = extract_field_setter_type(tp)
                if tp.type.fullname() == FOREIGN_KEY_FULLNAME:
                    ref_to_model = tp.args[0]
                    if isinstance(ref_to_model, Instance) and ref_to_model.type.has_base(MODEL_CLASS_FULLNAME):
                        primary_key_type = extract_primary_key_type(ref_to_model.type)
                        if not primary_key_type:
                            primary_key_type = AnyType(TypeOfAny.special_form)
                        expected_types[name + '_id'] = primary_key_type
                if field_type:
                    expected_types[name] = field_type

    primary_key_type = extract_primary_key_type(model)
    if not primary_key_type:
        # no explicit primary key, set pk to Any and add id
        primary_key_type = AnyType(TypeOfAny.special_form)
        expected_types['id'] = ctx.api.named_generic_type('builtins.int', [])

    expected_types['pk'] = primary_key_type
    return expected_types


def get_argument_by_name(ctx: FunctionContext, name: str) -> Optional[Expression]:
    """Return the expression for the specific argument.

    This helper should only be used with non-star arguments.
    """
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    args = ctx.args[idx]
    if len(args) != 1:
        # Either an error or no value passed.
        return None
    return args[0]


def get_argument_type_by_name(ctx: FunctionContext, name: str) -> Optional[Type]:
    """Return the type for the specific argument.

    This helper should only be used with non-star arguments.
    """
    if name not in ctx.callee_arg_names:
        return None
    idx = ctx.callee_arg_names.index(name)
    arg_types = ctx.arg_types[idx]
    if len(arg_types) != 1:
        # Either an error or no value passed.
        return None
    return arg_types[0]
