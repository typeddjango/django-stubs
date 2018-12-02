from typing import cast, Iterator, Tuple, Optional, Dict

from mypy.nodes import ClassDef, AssignmentStmt, CallExpr, MemberExpr, StrExpr, NameExpr, MDEF, TypeInfo, Var, SymbolTableNode, \
    Lvalue, Expression, MypyFile
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance

from mypy_django_plugin import helpers


def add_new_var_node_to_class(class_type: TypeInfo, name: str, typ: Instance) -> None:
    var = Var(name=name, type=typ)
    var.info = typ.type
    var._fullname = class_type.fullname() + '.' + name
    var.is_inferred = True
    var.is_initialized_in_class = True
    class_type.names[name] = SymbolTableNode(MDEF, var)


def iter_over_assignments(klass: ClassDef) -> Iterator[Tuple[Lvalue, Expression]]:
    for stmt in klass.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # not supported yet
            continue
        yield stmt.lvalues[0], stmt.rvalue


def iter_call_assignments(klass: ClassDef) -> Iterator[Tuple[Lvalue, CallExpr]]:
    for lvalue, rvalue in iter_over_assignments(klass):
        if isinstance(rvalue, CallExpr):
            yield lvalue, rvalue


def iter_over_one_to_n_related_fields(klass: ClassDef) -> Iterator[Tuple[NameExpr, CallExpr]]:
    for lvalue, rvalue in iter_call_assignments(klass):
        if (isinstance(lvalue, NameExpr)
                and isinstance(rvalue.callee, MemberExpr)):
            if rvalue.callee.fullname in {helpers.FOREIGN_KEY_FULLNAME,
                                          helpers.ONETOONE_FIELD_FULLNAME}:
                yield lvalue, rvalue


def get_nested_meta_class(model_type: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = model_type.names.get('Meta')
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def is_abstract_model(ctx: ClassDefContext) -> bool:
    meta_node = get_nested_meta_class(ctx.cls.info)
    if meta_node is None:
        return False

    for lvalue, rvalue in iter_over_assignments(meta_node.defn):
        if isinstance(lvalue, NameExpr) and lvalue.name == 'abstract':
            is_abstract = ctx.api.parse_bool(rvalue)
            if is_abstract:
                # abstract model do not need 'objects' queryset
                return True
    return False


def set_fieldname_attrs_for_related_fields(ctx: ClassDefContext) -> None:
    api = ctx.api
    for lvalue, rvalue in iter_over_one_to_n_related_fields(ctx.cls):
        property_name = lvalue.name + '_id'
        add_new_var_node_to_class(ctx.cls.info, property_name,
                                  typ=api.named_type('__builtins__.int'))


def add_int_id_attribute_if_primary_key_true_is_not_present(ctx: ClassDefContext) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    if is_abstract_model(ctx):
        return None

    for _, rvalue in iter_call_assignments(ctx.cls):
        if ('primary_key' in rvalue.arg_names and
                api.parse_bool(rvalue.args[rvalue.arg_names.index('primary_key')])):
            break
    else:
        add_new_var_node_to_class(ctx.cls.info, 'id', api.builtin_type('builtins.int'))


def set_objects_queryset_to_model_class(ctx: ClassDefContext) -> None:
    # search over mro
    objects_sym = ctx.cls.info.get('objects')
    if objects_sym is not None:
        return None

    # only direct Meta class
    if is_abstract_model(ctx):
        # abstract model do not need 'objects' queryset
        return None

    api = cast(SemanticAnalyzerPass2, ctx.api)
    typ = api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME,
                                 args=[Instance(ctx.cls.info, [])])
    if not typ:
        return None
    add_new_var_node_to_class(ctx.cls.info, 'objects', typ=typ)


def inject_any_as_base_for_nested_class_meta(ctx: ClassDefContext) -> None:
    meta_node = get_nested_meta_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def iter_over_classdefs(module_file: MypyFile) -> Iterator[ClassDef]:
    for defn in module_file.defs:
        if isinstance(defn, ClassDef):
            yield defn


def get_related_field_type(rvalue: CallExpr, api: SemanticAnalyzerPass2,
                           related_model_typ: TypeInfo) -> Optional[Instance]:
    if rvalue.callee.name == 'ForeignKey':
        return api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME,
                                      args=[Instance(related_model_typ, [])])
    else:
        return Instance(related_model_typ, [])


def is_related_field(expr: CallExpr, module_file: MypyFile) -> bool:
    if isinstance(expr.callee, MemberExpr) and isinstance(expr.callee.expr, NameExpr):
        module = module_file.names[expr.callee.expr.name]
        if module.fullname == 'django.db.models' and expr.callee.name in {'ForeignKey', 'OneToOneField'}:
            return True
    return False


def extract_ref_to_fullname(rvalue_expr: CallExpr,
                            module_file: MypyFile, all_modules: Dict[str, MypyFile]) -> Optional[str]:
    if 'to' in rvalue_expr.arg_names:
        to_expr = rvalue_expr.args[rvalue_expr.arg_names.index('to')]
    else:
        to_expr = rvalue_expr.args[0]
    if isinstance(to_expr, NameExpr):
        return module_file.names[to_expr.name].fullname
    elif isinstance(to_expr, StrExpr):
        typ_fullname = helpers.get_model_fullname_from_string(to_expr, all_modules)
        if typ_fullname is None:
            return None
        return typ_fullname
    return None


def add_related_managers(ctx: ClassDefContext):
    api = cast(SemanticAnalyzerPass2, ctx.api)
    for module_name, module_file in ctx.api.modules.items():
        for defn in iter_over_classdefs(module_file):
            for lvalue, rvalue in iter_call_assignments(defn):
                if is_related_field(rvalue, module_file):
                    ref_to_fullname = extract_ref_to_fullname(rvalue, module_file=module_file,
                                                              all_modules=api.modules)
                    if ctx.cls.fullname == ref_to_fullname:
                        if 'related_name' in rvalue.arg_names:
                            related_name_expr = rvalue.args[rvalue.arg_names.index('related_name')]
                            if not isinstance(related_name_expr, StrExpr):
                                return None
                            related_name = related_name_expr.value
                            typ = get_related_field_type(rvalue, api, defn.info)
                            if typ is None:
                                return None
                            add_new_var_node_to_class(ctx.cls.info, related_name, typ)


def process_model_class(ctx: ClassDefContext) -> None:
    add_related_managers(ctx)
    inject_any_as_base_for_nested_class_meta(ctx)
    set_fieldname_attrs_for_related_fields(ctx)
    add_int_id_attribute_if_primary_key_true_is_not_present(ctx)
    set_objects_queryset_to_model_class(ctx)
