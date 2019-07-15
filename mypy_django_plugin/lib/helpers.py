from collections import OrderedDict
from typing import Dict, Iterator, List, Optional, Set, TYPE_CHECKING, Tuple, Union, cast

from mypy.mro import calculate_mro
from mypy.nodes import (AssignmentStmt, Block, CallExpr, ClassDef, Expression, FakeInfo, GDEF, ImportedName, Lvalue, MDEF,
                        MemberExpr, MypyFile, NameExpr, SymbolNode, SymbolTable, SymbolTableNode, TypeInfo, Var)
from mypy.plugin import CheckerPluginInterface, FunctionContext, MethodContext
from mypy.types import (AnyType, Instance, NoneTyp, TupleType, Type as MypyType, TypeOfAny, TypeVarType, TypedDictType,
                        UnionType)

from mypy_django_plugin.lib import fullnames, metadata

if TYPE_CHECKING:
    from mypy.checker import TypeChecker


def get_models_file(app_name: str, all_modules: Dict[str, MypyFile]) -> Optional[MypyFile]:
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


class SameFileModel(Exception):
    def __init__(self, model_cls_name: str):
        self.model_cls_name = model_cls_name


class SelfReference(ValueError):
    pass


def get_model_fullname_from_string(model_string: str,
                                   all_modules: Dict[str, MypyFile]) -> Optional[str]:
    if model_string == 'self':
        raise SelfReference()

    if '.' not in model_string:
        raise SameFileModel(model_string)

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


def reparametrize_instance(instance: Instance, new_args: List[MypyType]) -> Instance:
    return Instance(instance.type, args=new_args,
                    line=instance.line, column=instance.column)


def fill_typevars_with_any(instance: Instance) -> Instance:
    return reparametrize_instance(instance, [AnyType(TypeOfAny.unannotated)])


def extract_typevar_value(tp: Instance, typevar_name: str) -> MypyType:
    if typevar_name in {'_T', '_T_co'}:
        if '_T' in tp.type.type_vars:
            return tp.args[tp.type.type_vars.index('_T')]
        if '_T_co' in tp.type.type_vars:
            return tp.args[tp.type.type_vars.index('_T_co')]
    return tp.args[tp.type.type_vars.index(typevar_name)]


def fill_typevars(tp: Instance, type_to_fill: Instance) -> Instance:
    typevar_values: List[MypyType] = []
    for typevar_arg in type_to_fill.args:
        if isinstance(typevar_arg, TypeVarType):
            typevar_values.append(extract_typevar_value(tp, typevar_arg.name))
    return Instance(type_to_fill.type, typevar_values)


def get_call_argument_by_name(ctx: Union[FunctionContext, MethodContext], name: str) -> Optional[Expression]:
    """
    Return the expression for the specific argument.
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


def get_call_argument_type_by_name(ctx: Union[FunctionContext, MethodContext], name: str) -> Optional[MypyType]:
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


def get_setting_expr(api: 'TypeChecker', setting_name: str) -> Optional[Expression]:
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
    for name_expr, value_expr in iter_over_module_level_assignments(module_file):
        if isinstance(name_expr, NameExpr) and name_expr.name == setting_name:
            return value_expr
    return None


def iter_over_class_level_assignments(klass: ClassDef) -> Iterator[Tuple[str, Expression]]:
    for stmt in klass.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # skip multiple assignments
            continue
        lvalue = stmt.lvalues[0]
        if isinstance(lvalue, NameExpr):
            yield lvalue.name, stmt.rvalue


def iter_over_module_level_assignments(module: MypyFile) -> Iterator[Tuple[str, Expression]]:
    for stmt in module.defs:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # skip multiple assignments
            continue
        lvalue = stmt.lvalues[0]
        if isinstance(lvalue, NameExpr):
            yield lvalue.name, stmt.rvalue


def iter_over_assignments_in_class(class_or_module: Union[ClassDef, MypyFile]
                                   ) -> Iterator[Tuple[str, Expression]]:
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
        lvalue = stmt.lvalues[0]
        if isinstance(lvalue, NameExpr):
            yield lvalue.name, stmt.rvalue


def extract_field_setter_type(tp: Instance) -> Optional[MypyType]:
    """ Extract __set__ value of a field. """
    if tp.type.has_base(fullnames.FIELD_FULLNAME):
        return tp.args[0]
    # GenericForeignKey
    if tp.type.has_base(fullnames.GENERIC_FOREIGN_KEY_FULLNAME):
        return AnyType(TypeOfAny.special_form)
    return None


def extract_field_getter_type(tp: MypyType) -> Optional[MypyType]:
    """ Extract return type of __get__ of subclass of Field"""
    if not isinstance(tp, Instance):
        return None
    if tp.type.has_base(fullnames.FIELD_FULLNAME):
        return tp.args[1]
    # GenericForeignKey
    if tp.type.has_base(fullnames.GENERIC_FOREIGN_KEY_FULLNAME):
        return AnyType(TypeOfAny.special_form)
    return None


def extract_explicit_set_type_of_model_primary_key(model: TypeInfo) -> Optional[MypyType]:
    """
    If field with primary_key=True is set on the model, extract its __set__ type.
    """
    for field_name, props in metadata.get_fields_metadata(model).items():
        is_primary_key = props.get('primary_key', False)
        if is_primary_key:
            return extract_field_setter_type(model.names[field_name].type)
    return None


def extract_primary_key_type_for_get(model: TypeInfo) -> Optional[MypyType]:
    for field_name, props in metadata.get_fields_metadata(model).items():
        is_primary_key = props.get('primary_key', False)
        if is_primary_key:
            return extract_field_getter_type(model.names[field_name].type)
    return None


def make_optional(typ: MypyType) -> MypyType:
    return UnionType.make_union([typ, NoneTyp()])


def make_required(typ: MypyType) -> MypyType:
    if not isinstance(typ, UnionType):
        return typ
    items = [item for item in typ.items if not isinstance(item, NoneTyp)]
    # will reduce to Instance, if only one item
    return UnionType.make_union(items)


def is_optional(typ: MypyType) -> bool:
    if not isinstance(typ, UnionType):
        return False

    return any([isinstance(item, NoneTyp) for item in typ.items])


def has_any_of_bases(info: TypeInfo, bases: Set[str]) -> bool:
    for base_fullname in bases:
        if info.has_base(base_fullname):
            return True
    return False


def is_none_expr(expr: Expression) -> bool:
    return isinstance(expr, NameExpr) and expr.fullname == 'builtins.None'


def get_nested_meta_node_for_current_class(info: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = info.names.get('Meta')
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def get_assignment_stmt_by_name(type_info: TypeInfo, name: str) -> Optional[Expression]:
    for assignment_name, call_expr in iter_over_class_level_assignments(type_info.defn):
        if assignment_name == name:
            return call_expr
    return None


def is_field_nullable(model: TypeInfo, field_name: str) -> bool:
    return metadata.get_fields_metadata(model).get(field_name, {}).get('null', False)


def is_foreign_key_like(t: MypyType) -> bool:
    if not isinstance(t, Instance):
        return False
    return has_any_of_bases(t.type, {fullnames.FOREIGN_KEY_FULLNAME, fullnames.ONETOONE_FIELD_FULLNAME})


def build_class_with_annotated_fields(api: 'TypeChecker', base: MypyType, fields: 'OrderedDict[str, MypyType]',
                                      name: str) -> Instance:
    """Build an Instance with `name` that contains the specified `fields` as attributes and extends `base`."""
    # Credit: This code is largely copied/modified from TypeChecker.intersect_instance_callable and
    # NamedTupleAnalyzer.build_namedtuple_typeinfo
    from mypy.checker import gen_unique_name

    cur_module = cast(MypyFile, api.scope.stack[0])
    gen_name = gen_unique_name(name, cur_module.names)

    cdef = ClassDef(name, Block([]))
    cdef.fullname = cur_module.fullname() + '.' + gen_name
    info = TypeInfo(SymbolTable(), cdef, cur_module.fullname())
    cdef.info = info
    info.bases = [base]

    def add_field(var: Var, is_initialized_in_class: bool = False,
                  is_property: bool = False) -> None:
        var.info = info
        var.is_initialized_in_class = is_initialized_in_class
        var.is_property = is_property
        var._fullname = '%s.%s' % (info.fullname(), var.name())
        info.names[var.name()] = SymbolTableNode(MDEF, var)

    vars = [Var(item, typ) for item, typ in fields.items()]
    for var in vars:
        add_field(var, is_property=True)

    calculate_mro(info)
    info.calculate_metaclass_type()

    cur_module.names[gen_name] = SymbolTableNode(GDEF, info, plugin_generated=True)
    return Instance(info, [])


def make_named_tuple(api: 'TypeChecker', fields: 'OrderedDict[str, MypyType]', name: str) -> MypyType:
    if not fields:
        # No fields specified, so fallback to a subclass of NamedTuple that allows
        # __getattr__ / __setattr__ for any attribute name.
        fallback = api.named_generic_type('django._NamedTupleAnyAttr', [])
    else:
        fallback = build_class_with_annotated_fields(
            api=api,
            base=api.named_generic_type('NamedTuple', []),
            fields=fields,
            name=name
        )
    return TupleType(list(fields.values()), fallback=fallback)


def make_typeddict(api: CheckerPluginInterface, fields: 'OrderedDict[str, MypyType]',
                   required_keys: Set[str]) -> TypedDictType:
    object_type = api.named_generic_type('mypy_extensions._TypedDict', [])
    typed_dict_type = TypedDictType(fields, required_keys=required_keys, fallback=object_type)
    return typed_dict_type


def make_tuple(api: 'TypeChecker', fields: List[MypyType]) -> TupleType:
    implicit_any = AnyType(TypeOfAny.special_form)
    fallback = api.named_generic_type('builtins.tuple', [implicit_any])
    return TupleType(fields, fallback=fallback)


def get_private_descriptor_type(type_info: TypeInfo, private_field_name: str, is_nullable: bool) -> MypyType:
    node = type_info.get(private_field_name).node
    if isinstance(node, Var):
        descriptor_type = node.type
        if is_nullable:
            descriptor_type = make_optional(descriptor_type)
        return descriptor_type
    return AnyType(TypeOfAny.unannotated)


class IncompleteDefnException(Exception):
    pass


def iter_over_toplevel_classes(module_file: MypyFile) -> Iterator[ClassDef]:
    for defn in module_file.defs:
        if isinstance(defn, ClassDef):
            yield defn


def iter_call_assignments_in_class(klass: ClassDef) -> Iterator[Tuple[str, CallExpr]]:
    for name, expression in iter_over_assignments_in_class(klass):
        if isinstance(expression, CallExpr):
            yield name, expression


def iter_over_field_inits_in_class(klass: ClassDef) -> Iterator[Tuple[str, CallExpr]]:
    for lvalue, rvalue in iter_over_assignments_in_class(klass):
        if isinstance(lvalue, NameExpr) and isinstance(rvalue, CallExpr):
            field_name = lvalue.name
            if isinstance(rvalue.callee, MemberExpr) and isinstance(rvalue.callee.node, TypeInfo):
                if isinstance(rvalue.callee.node, FakeInfo):
                    raise IncompleteDefnException()

                field_info = rvalue.callee.node
                if field_info.has_base(fullnames.FIELD_FULLNAME):
                    yield field_name, rvalue


def get_related_manager_type_from_metadata(model_info: TypeInfo, related_manager_name: str,
                                           api: CheckerPluginInterface) -> Optional[Instance]:
    related_manager_metadata = metadata.get_related_managers_metadata(model_info)
    if not related_manager_metadata:
        return None

    if related_manager_name not in related_manager_metadata:
        return None

    manager_class_name = related_manager_metadata[related_manager_name]['manager']
    of = related_manager_metadata[related_manager_name]['of']
    of_types = []
    for of_type_name in of:
        if of_type_name == 'any':
            of_types.append(AnyType(TypeOfAny.implementation_artifact))
        else:
            try:
                of_type = api.named_generic_type(of_type_name, [])
            except AssertionError:
                # Internal error: attempted lookup of unknown name
                of_type = AnyType(TypeOfAny.implementation_artifact)

            of_types.append(of_type)

    return api.named_generic_type(manager_class_name, of_types)


def get_primary_key_field_name(model_info: TypeInfo) -> Optional[str]:
    for base in model_info.mro:
        fields = metadata.get_fields_metadata(base)
        for field_name, field_props in fields.items():
            is_primary_key = field_props.get('primary_key', False)
            if is_primary_key:
                return field_name
    return None


def _get_app_models_file(app_name: str, all_modules: Dict[str, MypyFile]) -> Optional[MypyFile]:
    models_module = '.'.join([app_name, 'models'])
    return all_modules.get(models_module)


def get_model_info(app_name_dot_model_name: str, all_modules: Dict[str, MypyFile]) -> Optional[TypeInfo]:
    """ Resolve app_name.ModelName into model fullname """
    app_name, model_name = app_name_dot_model_name.split('.')
    models_file = _get_app_models_file(app_name, all_modules)
    if models_file is None:
        return None

    sym = models_file.names.get(model_name)
    if sym and isinstance(sym.node, TypeInfo):
        return sym.node
