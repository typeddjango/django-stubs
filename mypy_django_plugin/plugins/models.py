from typing import cast, Iterator, Tuple, Optional

from mypy.nodes import ClassDef, AssignmentStmt, CallExpr, MemberExpr, StrExpr, NameExpr, MDEF, TypeInfo, Var, SymbolTableNode, \
    Lvalue, Expression, Statement
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
        if not isinstance(rvalue, CallExpr):
            continue
        yield lvalue, rvalue


def iter_over_one_to_n_related_fields(klass: ClassDef, api: SemanticAnalyzerPass2) -> Iterator[Tuple[NameExpr, CallExpr]]:
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
    for lvalue, rvalue in iter_over_one_to_n_related_fields(ctx.cls, api):
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


def is_model_defn(defn: Statement, api: SemanticAnalyzerPass2) -> bool:
    if not isinstance(defn, ClassDef):
        return False

    for base_type_expr in defn.base_type_exprs:
        # api.accept(base_type_expr)
        fullname = getattr(base_type_expr, 'fullname', None)
        if fullname == helpers.MODEL_CLASS_FULLNAME:
            return True
    return False


def iter_over_models(ctx: ClassDefContext) -> Iterator[ClassDef]:
    for module_name, module_file in ctx.api.modules.items():
        for defn in module_file.defs:
            if is_model_defn(defn, api=cast(SemanticAnalyzerPass2, ctx.api)):
                yield defn


def extract_to_value_or_none(field_expr: CallExpr, ctx: ClassDefContext) -> Optional[TypeInfo]:
    if 'to' in field_expr.arg_names:
        ref_expr = field_expr.args[field_expr.arg_names.index('to')]
    else:
        # first positional argument
        ref_expr = field_expr.args[0]

    if isinstance(ref_expr, StrExpr):
        model_typeinfo = helpers.get_model_type_from_string(ref_expr,
                                                            all_modules=ctx.api.modules)
        return model_typeinfo
    elif isinstance(ref_expr, NameExpr):
        return ref_expr.node


def get_related_field_type(rvalue: CallExpr, api: SemanticAnalyzerPass2,
                           related_model_typ: TypeInfo) -> Optional[Instance]:
    if rvalue.callee.fullname == helpers.FOREIGN_KEY_FULLNAME:
        return api.named_type_or_none(helpers.QUERYSET_CLASS_FULLNAME,
                                      args=[Instance(related_model_typ, [])])
    else:
        return Instance(related_model_typ, [])


def add_related_managers(ctx: ClassDefContext) -> None:
    for model_defn in iter_over_models(ctx):
        for _, rvalue in iter_over_one_to_n_related_fields(model_defn, ctx.api):
            if 'related_name' not in rvalue.arg_names:
                # positional related_name is not supported yet
                return
            related_name = rvalue.args[rvalue.arg_names.index('related_name')].value
            ref_to_typ = extract_to_value_or_none(rvalue, ctx)
            if ref_to_typ is not None:
                if ref_to_typ.fullname() == ctx.cls.info.fullname():
                    typ = get_related_field_type(rvalue, ctx.api,
                                                 related_model_typ=model_defn.info)
                    if typ is None:
                        return
                    add_new_var_node_to_class(ctx.cls.info, related_name, typ)


def process_model_class(ctx: ClassDefContext) -> None:
    # add_related_managers(ctx)
    inject_any_as_base_for_nested_class_meta(ctx)
    set_fieldname_attrs_for_related_fields(ctx)
    add_int_id_attribute_if_primary_key_true_is_not_present(ctx)
    set_objects_queryset_to_model_class(ctx)
