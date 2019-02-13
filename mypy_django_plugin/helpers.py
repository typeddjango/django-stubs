import typing
from typing import Dict, Optional

from mypy.checker import TypeChecker
from mypy.nodes import AssignmentStmt, ClassDef, Expression, FuncDef, ImportedName, Lvalue, MypyFile, NameExpr, SymbolNode, \
    TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import AnyType, CallableType, Instance, Type, TypeOfAny, TypeVarType, UnionType

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


def extract_typevar_value(tp: Instance, typevar_name: str) -> Type:
    if typevar_name in {'_T', '_T_co'}:
        if '_T' in tp.type.type_vars:
            return tp.args[tp.type.type_vars.index('_T')]
        if '_T_co' in tp.type.type_vars:
            return tp.args[tp.type.type_vars.index('_T_co')]
    return tp.args[tp.type.type_vars.index(typevar_name)]


def fill_typevars(tp: Instance, type_to_fill: Instance) -> Instance:
    typevar_values: typing.List[Type] = []
    for typevar_arg in type_to_fill.args:
        if isinstance(typevar_arg, TypeVarType):
            typevar_values.append(extract_typevar_value(tp, typevar_arg.name))
    return reparametrize_with(type_to_fill, typevar_values)


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


def get_setting_expr(api: TypeChecker, setting_name: str) -> Optional[Expression]:
    try:
        settings_sym = api.modules['django.conf'].names['settings']
    except KeyError:
        return None

    settings_type: TypeInfo = settings_sym.type.type
    auth_user_model_sym = settings_type.get(setting_name)
    if not auth_user_model_sym:
        return None

    module, _, name = auth_user_model_sym.fullname.rpartition('.')
    if module not in api.modules:
        return None

    module_file = api.modules.get(module)
    for name_expr, value_expr in iter_over_assignments(module_file):
        if isinstance(name_expr, NameExpr) and name_expr.name == setting_name:
            return value_expr
    return None


def iter_over_assignments(
    class_or_module: typing.Union[ClassDef, MypyFile]) -> typing.Iterator[typing.Tuple[Lvalue, Expression]]:
    if isinstance(class_or_module, ClassDef):
        statements = class_or_module.defs.body
    else:
        statements = class_or_module.defs

    for stmt in statements:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # not supported yet
            continue
        yield stmt.lvalues[0], stmt.rvalue


def extract_field_setter_type(tp: Instance) -> Optional[Type]:
    if not isinstance(tp, Instance):
        return None
    if tp.type.has_base(FIELD_FULLNAME):
        set_method = tp.type.get_method('__set__')
        if isinstance(set_method, FuncDef) and isinstance(set_method.type, CallableType):
            if 'value' in set_method.type.arg_names:
                set_value_type = set_method.type.arg_types[set_method.type.arg_names.index('value')]
                if isinstance(set_value_type, Instance):
                    set_value_type = fill_typevars(tp, set_value_type)
                    return set_value_type
                elif isinstance(set_value_type, UnionType):
                    items_no_typevars = []
                    for item in set_value_type.items:
                        if isinstance(item, Instance):
                            item = fill_typevars(tp, item)
                        items_no_typevars.append(item)
                    return UnionType(items_no_typevars)

    field_getter_type = extract_field_getter_type(tp)
    if field_getter_type:
        return field_getter_type

    return None


def extract_field_getter_type(tp: Instance) -> Optional[Type]:
    if not isinstance(tp, Instance):
        return None
    if tp.type.has_base(FIELD_FULLNAME):
        get_method = tp.type.get_method('__get__')
        if isinstance(get_method, FuncDef) and isinstance(get_method.type, CallableType):
            return get_method.type.ret_type
    # GenericForeignKey
    if tp.type.has_base(GENERIC_FOREIGN_KEY_FULLNAME):
        return AnyType(TypeOfAny.special_form)
    return None


def get_django_metadata(model: TypeInfo) -> Dict[str, typing.Any]:
    return model.metadata.setdefault('django', {})


def get_related_field_primary_key_names(base_model: TypeInfo) -> typing.List[str]:
    django_metadata = get_django_metadata(base_model)
    return django_metadata.setdefault('related_field_primary_keys', [])


def get_fields_metadata(model: TypeInfo) -> Dict[str, typing.Any]:
    return get_django_metadata(model).setdefault('fields', {})


def extract_primary_key_type_for_set(model: TypeInfo) -> Optional[Type]:
    for field_name, props in get_fields_metadata(model).items():
        is_primary_key = props.get('primary_key', False)
        if is_primary_key:
            return extract_field_setter_type(model.names[field_name].type)
    return None


def extract_primary_key_type_for_get(model: TypeInfo) -> Optional[Type]:
    for field_name, props in get_fields_metadata(model).items():
        is_primary_key = props.get('primary_key', False)
        if is_primary_key:
            return extract_field_getter_type(model.names[field_name].type)
    return None
