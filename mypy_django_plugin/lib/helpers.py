from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Literal, Optional, Set, Union, cast

from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy import checker
from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    GDEF,
    MDEF,
    AssignmentStmt,
    Block,
    ClassDef,
    Context,
    Expression,
    MemberExpr,
    MypyFile,
    NameExpr,
    StrExpr,
    SymbolNode,
    SymbolTable,
    SymbolTableNode,
    TypeInfo,
    Var,
)
from mypy.plugin import (
    AttributeContext,
    CheckerPluginInterface,
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    MethodContext,
    SemanticAnalyzerPluginInterface,
)
from mypy.semanal import SemanticAnalyzer
from mypy.types import AnyType, Instance, LiteralType, NoneTyp, TupleType, TypedDictType, TypeOfAny, UnionType
from mypy.types import Type as MypyType
from typing_extensions import TypedDict

from mypy_django_plugin.lib import fullnames
from mypy_django_plugin.lib.fullnames import WITH_ANNOTATIONS_FULLNAME

if TYPE_CHECKING:
    from mypy_django_plugin.django.context import DjangoContext


class DjangoTypeMetadata(TypedDict, total=False):
    is_abstract_model: bool
    from_queryset_manager: str
    reverse_managers: Dict[str, str]
    baseform_bases: Dict[str, int]
    manager_bases: Dict[str, int]
    model_bases: Dict[str, int]
    queryset_bases: Dict[str, int]
    m2m_throughs: Dict[str, str]


def get_django_metadata(model_info: TypeInfo) -> DjangoTypeMetadata:
    return cast(DjangoTypeMetadata, model_info.metadata.setdefault("django", {}))


def get_django_metadata_bases(
    model_info: TypeInfo, key: Literal["baseform_bases", "manager_bases", "queryset_bases"]
) -> Dict[str, int]:
    return get_django_metadata(model_info).setdefault(key, cast(Dict[str, int], {}))


class IncompleteDefnException(Exception):
    pass


def lookup_fully_qualified_sym(fullname: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolTableNode]:
    if "." not in fullname:
        return None
    if "[" in fullname and "]" in fullname:
        # We sometimes generate fake fullnames like a.b.C[x.y.Z] to provide a better representation to users
        # Make sure that we handle lookups of those types of names correctly if the part inside [] contains "."
        bracket_start = fullname.index("[")
        fullname_without_bracket = fullname[:bracket_start]
        module, cls_name = fullname_without_bracket.rsplit(".", 1)
        cls_name += fullname[bracket_start:]
    else:
        module, cls_name = fullname.rsplit(".", 1)

    parent_classes: List[str] = []
    while True:
        module_file = all_modules.get(module)
        if module_file:
            break
        if "." not in module:
            return None
        module, parent_cls = module.rsplit(".", 1)
        parent_classes.insert(0, parent_cls)

    scope: Union[MypyFile, TypeInfo] = module_file
    for parent_cls in parent_classes:
        sym = scope.names.get(parent_cls)
        if sym is None:
            return None
        if isinstance(sym.node, TypeInfo):
            scope = sym.node
        else:
            return None

    sym = scope.names.get(cls_name)
    if sym is None:
        return None
    return sym


def lookup_fully_qualified_generic(name: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolNode]:
    sym = lookup_fully_qualified_sym(name, all_modules)
    if sym is None:
        return None
    return sym.node


def lookup_fully_qualified_typeinfo(api: Union[TypeChecker, SemanticAnalyzer], fullname: str) -> Optional[TypeInfo]:
    node = lookup_fully_qualified_generic(fullname, api.modules)
    if not isinstance(node, TypeInfo):
        return None
    return node


def lookup_class_typeinfo(api: TypeChecker, klass: Optional[type]) -> Optional[TypeInfo]:
    if klass is None:
        return None

    fullname = get_class_fullname(klass)
    field_info = lookup_fully_qualified_typeinfo(api, fullname)
    return field_info


def reparametrize_instance(instance: Instance, new_args: List[MypyType]) -> Instance:
    return Instance(instance.type, args=new_args, line=instance.line, column=instance.column)


def get_class_fullname(klass: type) -> str:
    return klass.__module__ + "." + klass.__qualname__


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


def make_optional(typ: MypyType) -> MypyType:
    return UnionType.make_union([typ, NoneTyp()])


# Duplicating mypy.semanal_shared.parse_bool because importing it directly caused ImportError (#1784)
def parse_bool(expr: Expression) -> Optional[bool]:
    if isinstance(expr, NameExpr):
        if expr.fullname == "builtins.True":
            return True
        if expr.fullname == "builtins.False":
            return False
    return None


def has_any_of_bases(info: TypeInfo, bases: Iterable[str]) -> bool:
    for base_fullname in bases:
        if info.has_base(base_fullname):
            return True
    return False


def iter_bases(info: TypeInfo) -> Iterator[Instance]:
    for base in info.bases:
        yield base
        yield from iter_bases(base.type)


def get_private_descriptor_type(type_info: TypeInfo, private_field_name: str, is_nullable: bool) -> MypyType:
    """Return declared type of type_info's private_field_name (used for private Field attributes)"""
    sym = type_info.get(private_field_name)
    if sym is None:
        return AnyType(TypeOfAny.explicit)

    node = sym.node
    if isinstance(node, Var):
        descriptor_type = node.type
        if descriptor_type is None:
            return AnyType(TypeOfAny.explicit)

        if is_nullable:
            descriptor_type = make_optional(descriptor_type)
        return descriptor_type
    return AnyType(TypeOfAny.explicit)


def get_field_lookup_exact_type(api: TypeChecker, field: "Field[Any, Any]") -> MypyType:
    if isinstance(field, (RelatedField, ForeignObjectRel)):
        # Not using field.related_model because that may have str value "self"
        lookup_type_class = field.remote_field.model
        rel_model_info = lookup_class_typeinfo(api, lookup_type_class)
        if rel_model_info is None:
            return AnyType(TypeOfAny.from_error)
        return make_optional(Instance(rel_model_info, []))

    field_info = lookup_class_typeinfo(api, field.__class__)
    if field_info is None:
        return AnyType(TypeOfAny.explicit)
    return get_private_descriptor_type(field_info, "_pyi_lookup_exact_type", is_nullable=field.null)


def get_nested_meta_node_for_current_class(info: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = info.names.get("Meta")
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def is_annotated_model_fullname(model_cls_fullname: str) -> bool:
    return model_cls_fullname.startswith(WITH_ANNOTATIONS_FULLNAME + "[")


def create_type_info(name: str, module: str, bases: List[Instance]) -> TypeInfo:
    # make new class expression
    classdef = ClassDef(name, Block([]))
    classdef.fullname = module + "." + name

    # make new TypeInfo
    new_typeinfo = TypeInfo(SymbolTable(), classdef, module)
    new_typeinfo.bases = bases
    calculate_mro(new_typeinfo)
    new_typeinfo.calculate_metaclass_type()

    classdef.info = new_typeinfo

    return new_typeinfo


def add_new_class_for_module(
    module: MypyFile,
    name: str,
    bases: List[Instance],
    fields: Optional[Dict[str, MypyType]] = None,
    no_serialize: bool = False,
) -> TypeInfo:
    new_class_unique_name = checker.gen_unique_name(name, module.names)

    new_typeinfo = create_type_info(new_class_unique_name, module.fullname, bases)

    # add fields
    if fields:
        for field_name, field_type in fields.items():
            var = Var(field_name, type=field_type)
            var.info = new_typeinfo
            var._fullname = new_typeinfo.fullname + "." + field_name
            new_typeinfo.names[field_name] = SymbolTableNode(
                MDEF, var, plugin_generated=True, no_serialize=no_serialize
            )

    module.names[new_class_unique_name] = SymbolTableNode(
        GDEF, new_typeinfo, plugin_generated=True, no_serialize=no_serialize
    )
    return new_typeinfo


def get_current_module(api: TypeChecker) -> MypyFile:
    current_module = None
    for item in reversed(api.scope.stack):
        if isinstance(item, MypyFile):
            current_module = item
            break
    assert current_module is not None
    return current_module


def make_oneoff_named_tuple(
    api: TypeChecker, name: str, fields: "OrderedDict[str, MypyType]", extra_bases: Optional[List[Instance]] = None
) -> TupleType:
    current_module = get_current_module(api)
    if extra_bases is None:
        extra_bases = []
    namedtuple_info = add_new_class_for_module(
        current_module, name, bases=[api.named_generic_type("typing.NamedTuple", [])] + extra_bases, fields=fields
    )
    return TupleType(list(fields.values()), fallback=Instance(namedtuple_info, []))


def make_tuple(api: "TypeChecker", fields: List[MypyType]) -> TupleType:
    # fallback for tuples is any builtins.tuple instance
    fallback = api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.special_form)])
    return TupleType(fields, fallback=fallback)


def convert_any_to_type(typ: MypyType, referred_to_type: MypyType) -> MypyType:
    if isinstance(typ, UnionType):
        converted_items = []
        for item in typ.items:
            converted_items.append(convert_any_to_type(item, referred_to_type))
        return UnionType.make_union(converted_items, line=typ.line, column=typ.column)
    if isinstance(typ, Instance):
        args = []
        for default_arg in typ.args:
            if isinstance(default_arg, AnyType):
                args.append(referred_to_type)
            else:
                args.append(default_arg)
        return reparametrize_instance(typ, args)

    if isinstance(typ, AnyType):
        return referred_to_type

    return typ


def make_typeddict(
    api: CheckerPluginInterface, fields: "OrderedDict[str, MypyType]", required_keys: Set[str]
) -> TypedDictType:
    fallback_type = api.named_generic_type("typing._TypedDict", [])
    typed_dict_type = TypedDictType(fields, required_keys=required_keys, fallback=fallback_type)
    return typed_dict_type


def resolve_string_attribute_value(attr_expr: Expression, django_context: "DjangoContext") -> Optional[str]:
    if isinstance(attr_expr, StrExpr):
        return attr_expr.value

    # support extracting from settings, in general case it's unresolvable yet
    if isinstance(attr_expr, MemberExpr):
        member_name = attr_expr.name
        if isinstance(attr_expr.expr, NameExpr) and attr_expr.expr.fullname == "django.conf.settings":
            if hasattr(django_context.settings, member_name):
                return getattr(django_context.settings, member_name)  # type: ignore[no-any-return]
    return None


def get_semanal_api(ctx: Union[ClassDefContext, DynamicClassDefContext]) -> SemanticAnalyzer:
    if not isinstance(ctx.api, SemanticAnalyzer):
        raise ValueError("Not a SemanticAnalyzer")
    return ctx.api


def get_typechecker_api(ctx: Union[AttributeContext, MethodContext, FunctionContext]) -> TypeChecker:
    if not isinstance(ctx.api, TypeChecker):
        raise ValueError("Not a TypeChecker")
    return ctx.api


def is_model_subclass_info(info: TypeInfo, django_context: "DjangoContext") -> bool:
    return info.fullname in django_context.all_registered_model_class_fullnames or info.has_base(
        fullnames.MODEL_CLASS_FULLNAME
    )


def check_types_compatible(
    ctx: Union[FunctionContext, MethodContext], *, expected_type: MypyType, actual_type: MypyType, error_message: str
) -> None:
    api = get_typechecker_api(ctx)
    api.check_subtype(actual_type, expected_type, ctx.context, error_message, "got", "expected")


def add_new_sym_for_info(
    info: TypeInfo, name: str, sym_type: MypyType, *, no_serialize: bool = False, is_classvar: bool = False
) -> None:
    # type=: type of the variable itself
    var = Var(name=name, type=sym_type)
    # var.info: type of the object variable is bound to
    var.info = info
    var._fullname = info.fullname + "." + name
    var.is_initialized_in_class = True
    var.is_inferred = True
    var.is_classvar = is_classvar
    info.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True, no_serialize=no_serialize)


def add_new_manager_base(api: SemanticAnalyzerPluginInterface, fullname: str) -> None:
    sym = api.lookup_fully_qualified_or_none(fullnames.MANAGER_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        bases = get_django_metadata_bases(sym.node, "manager_bases")
        bases[fullname] = 1


def is_abstract_model(model: TypeInfo) -> bool:
    if model.metaclass_type is None or model.metaclass_type.type.fullname != fullnames.MODEL_METACLASS_FULLNAME:
        return False

    metadata = get_django_metadata(model)
    if metadata.get("is_abstract_model") is not None:
        return metadata["is_abstract_model"]

    meta = model.names.get("Meta")
    # Check if 'abstract' is declared in this model's 'class Meta' as
    # 'abstract = True' won't be inherited from a parent model.
    if meta is not None and isinstance(meta.node, TypeInfo) and "abstract" in meta.node.names:
        for stmt in meta.node.defn.defs.body:
            if (
                # abstract =
                isinstance(stmt, AssignmentStmt)
                and len(stmt.lvalues) == 1
                and isinstance(stmt.lvalues[0], NameExpr)
                and stmt.lvalues[0].name == "abstract"
            ):
                # abstract = True (builtins.bool)
                rhs_is_true = parse_bool(stmt.rvalue) is True
                # abstract: Literal[True]
                is_literal_true = isinstance(stmt.type, LiteralType) and stmt.type.value is True
                metadata["is_abstract_model"] = rhs_is_true or is_literal_true
                return metadata["is_abstract_model"]

    metadata["is_abstract_model"] = False
    return False


def resolve_lazy_reference(
    reference: str, *, api: Union[TypeChecker, SemanticAnalyzer], django_context: "DjangoContext", ctx: Context
) -> Optional[TypeInfo]:
    """
    Attempts to resolve a lazy reference(e.g. "<app_label>.<object_name>") to a
    'TypeInfo' instance.
    """
    if "." not in reference:
        # <object_name> -- needs prefix of <app_label>. We can't implicitly solve
        # what app label this should be, yet.
        return None

    # Reference conforms to the structure of a lazy reference: '<app_label>.<object_name>'
    fullname = django_context.model_class_fullnames_by_label.get(reference)
    if fullname is not None:
        model_info = lookup_fully_qualified_typeinfo(api, fullname)
        if model_info is not None:
            return model_info
        elif isinstance(api, SemanticAnalyzer) and not api.final_iteration:
            # Getting this far, where Django matched the reference but we still can't
            # find it, we want to defer
            api.defer()
    else:
        api.fail("Could not match lazy reference with any model", ctx)
    return None
