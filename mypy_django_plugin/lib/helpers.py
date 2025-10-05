from collections.abc import Iterable, Iterator
from typing import TYPE_CHECKING, Any, Literal, NamedTuple, TypedDict, cast

from django.db.models.base import Model
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy import checker
from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    GDEF,
    MDEF,
    ArgKind,
    AssignmentStmt,
    Block,
    CallExpr,
    ClassDef,
    Context,
    Expression,
    MemberExpr,
    MypyFile,
    NameExpr,
    Node,
    RefExpr,
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
)
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import make_optional_type
from mypy.types import (
    AnyType,
    CallableType,
    ExtraAttrs,
    Instance,
    LiteralType,
    NoneTyp,
    TupleType,
    Type,
    TypedDictType,
    TypeOfAny,
    UnionType,
    get_proper_type,
)
from mypy.types import Type as MypyType
from typing_extensions import Self

from mypy_django_plugin.lib import fullnames

if TYPE_CHECKING:
    from django.db.models.fields import Field

    from mypy_django_plugin.django.context import DjangoContext


class DjangoTypeMetadata(TypedDict, total=False):
    is_abstract_model: bool
    is_annotated_model: bool
    from_queryset_manager: str
    reverse_managers: dict[str, str]
    baseform_bases: dict[str, int]
    m2m_throughs: dict[str, str]
    m2m_managers: dict[str, str]
    manager_to_model: str


def get_django_metadata(model_info: TypeInfo) -> DjangoTypeMetadata:
    return cast("DjangoTypeMetadata", model_info.metadata.setdefault("django", {}))


def get_django_metadata_bases(model_info: TypeInfo, key: Literal["baseform_bases"]) -> dict[str, int]:
    return get_django_metadata(model_info).setdefault(key, cast("dict[str, int]", {}))


def get_reverse_manager_info(
    api: TypeChecker | SemanticAnalyzer, model_info: TypeInfo, derived_from: str
) -> TypeInfo | None:
    manager_fullname = get_django_metadata(model_info).get("reverse_managers", {}).get(derived_from)
    if not manager_fullname:
        return None

    return lookup_fully_qualified_typeinfo(api, manager_fullname)


def set_reverse_manager_info(model_info: TypeInfo, derived_from: str, fullname: str) -> None:
    get_django_metadata(model_info).setdefault("reverse_managers", {})[derived_from] = fullname


def get_many_to_many_manager_info(
    api: TypeChecker | SemanticAnalyzer, *, to: TypeInfo, derived_from: str
) -> TypeInfo | None:
    manager_fullname = get_django_metadata(to).get("m2m_managers", {}).get(derived_from)
    if not manager_fullname:
        return None

    return lookup_fully_qualified_typeinfo(api, manager_fullname)


def set_many_to_many_manager_info(to: TypeInfo, derived_from: str, manager_info: TypeInfo) -> None:
    get_django_metadata(to).setdefault("m2m_managers", {})[derived_from] = manager_info.fullname


def mark_as_annotated_model(model: TypeInfo) -> None:
    get_django_metadata(model)["is_annotated_model"] = True


def is_annotated_model(model: TypeInfo) -> bool:
    return get_django_metadata(model).get("is_annotated_model", False)


class IncompleteDefnException(Exception):
    pass


def lookup_fully_qualified_sym(fullname: str, all_modules: dict[str, MypyFile]) -> SymbolTableNode | None:
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

    parent_classes: list[str] = []
    while True:
        module_file = all_modules.get(module)
        if module_file:
            break
        if "." not in module:
            return None
        module, parent_cls = module.rsplit(".", 1)
        parent_classes.insert(0, parent_cls)

    scope: MypyFile | TypeInfo = module_file
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


def lookup_fully_qualified_generic(name: str, all_modules: dict[str, MypyFile]) -> SymbolNode | None:
    sym = lookup_fully_qualified_sym(name, all_modules)
    if sym is None:
        return None
    return sym.node


def lookup_fully_qualified_typeinfo(api: TypeChecker | SemanticAnalyzer, fullname: str) -> TypeInfo | None:
    node = lookup_fully_qualified_generic(fullname, api.modules)
    if not isinstance(node, TypeInfo):
        return None
    return node


def lookup_class_typeinfo(api: TypeChecker, klass: type | None) -> TypeInfo | None:
    if klass is None:
        return None

    fullname = get_class_fullname(klass)
    return lookup_fully_qualified_typeinfo(api, fullname)


def get_class_fullname(klass: type) -> str:
    return klass.__module__ + "." + klass.__qualname__


def get_min_argument_count(ctx: MethodContext | FunctionContext) -> int:
    """
    Return the number of non-star arguments passed to the function.
    Excludes *args and **kwargs since their count is indeterminate.
    """
    return sum(not kind.is_star() for kinds in ctx.arg_kinds for kind in kinds)


class DjangoModel(NamedTuple):
    """A small wrapper around a django model runtime object and associated mypy type info"""

    # The Django model at runtime
    cls: type[Model]
    # The associated Mypy Instance
    typ: Instance
    # Is an annotated variant of a model ie `MyModel@AnnotatedWith`. See `AddAnnotateUtilities`
    is_annotated: bool

    @property
    def info(self) -> TypeInfo:
        return self.typ.type

    @classmethod
    def from_model_type(cls, model_type: Instance, django_context: "DjangoContext") -> Self | None:
        model_info = model_type.type
        is_annotated = is_annotated_model(model_info)

        model_cls = (
            django_context.get_model_class_by_fullname(model_info.bases[0].type.fullname)
            if is_annotated
            else django_context.get_model_class_by_fullname(model_info.fullname)
        )
        if model_cls is None:
            return None

        return cls(cls=model_cls, typ=model_type, is_annotated=is_annotated)


def extract_model_type_from_queryset(queryset_type: Instance, api: TypeChecker) -> Instance | None:
    """Extract the django model `Instance` associated to a queryset `Instance`"""
    for base_type in [queryset_type, *queryset_type.type.bases]:
        if (
            # Queryset/Manager subclasses providing the model type as a type param
            # Ex:
            #     class MyQuerySet(models.QuerySet[MyModel]):
            #         ...
            not len(base_type.args)
            # Manager generated by `ProcessManyToManyFields.create_many_related_manager`
            # type param is the Through model, not the model associated with the queryset.
            # We need to skip in that case to get it from the parent `ManyRelatedManager` Instance.
            or base_type.type.has_base(fullnames.MANY_RELATED_MANAGER)
        ):
            continue
        model = get_proper_type(base_type.args[0])
        if isinstance(model, Instance) and is_model_type(model.type):
            return model
    return None


def get_model_info_from_qs_ctx(
    ctx: MethodContext,
    django_context: "DjangoContext",
) -> DjangoModel | None:
    """
    Extract DjangoModel details from a queryset/manager `MethodContext`
    """
    api = get_typechecker_api(ctx)
    if not (isinstance(ctx.type, Instance) and (model_type := extract_model_type_from_queryset(ctx.type, api))):
        return None

    return DjangoModel.from_model_type(model_type, django_context)


def _get_class_init_type(call: CallExpr) -> CallableType | None:
    callee_node: Node | None = call.callee

    if isinstance(callee_node, RefExpr):
        callee_node = callee_node.node

    if (
        isinstance(callee_node, TypeInfo)
        and (init_sym := callee_node.get("__init__"))
        and isinstance((init_type := get_proper_type(init_sym.type)), CallableType)
    ):
        return init_type
    return None


def get_class_init_argument_by_name(call: CallExpr, name: str) -> Expression | None:
    """Adaptation of `mypy.plugins.common._get_argument` for class initializers"""
    callee_type = _get_class_init_type(call)
    if not callee_type:
        return None

    argument = callee_type.argument_by_name(name)
    if not argument:
        return None
    assert argument.name

    for i, (attr_name, attr_value) in enumerate(
        zip(call.arg_names, call.args, strict=False),
        start=1,  # Start at one to skip first `self` arg
    ):
        if argument.pos is not None and not attr_name and i == argument.pos:
            return attr_value
        if attr_name == argument.name:
            return attr_value

    return None


def get_call_argument_by_name(ctx: FunctionContext | MethodContext, name: str) -> Expression | None:
    """
    Return the expression for the specific argument.
    This helper supports named and positional arguments and should only be used with non-star arguments.

    Ex:
        Given `def my_func(a: int, b: str), `get_call_argument_by_name(ctx, "b")` works for`
        - `my_func(1, b="x")`
        - `my_func(1, "x")`
    """
    # try and pull the named argument from the caller first
    for kinds, argnames, args in zip(ctx.arg_kinds, ctx.arg_names, ctx.args, strict=False):
        for kind, argname, arg in zip(kinds, argnames, args, strict=False):
            if kind == ArgKind.ARG_NAMED and argname == name:
                return arg

    if name not in ctx.callee_arg_names:
        return None

    idx = ctx.callee_arg_names.index(name)
    args = ctx.args[idx]
    if len(args) != 1:
        # Either an error or no value passed.
        return None
    return args[0]


def get_bool_call_argument_by_name(ctx: FunctionContext | MethodContext, name: str, *, default: bool) -> bool:
    """
    Return the boolean value for an argument or the default if it's not found.
    """
    arg_value = get_call_argument_by_name(ctx, name)
    if arg_value is not None:
        parsed_value = parse_bool(arg_value)
        if parsed_value is not None:
            return parsed_value
    return default


def get_call_argument_type_by_name(ctx: FunctionContext | MethodContext, name: str) -> MypyType | None:
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


def is_optional(typ: MypyType) -> bool:
    typ = get_proper_type(typ)
    return isinstance(typ, UnionType) and any(isinstance(get_proper_type(item), NoneTyp) for item in typ.items)


# Duplicating mypy.semanal_shared.parse_bool because importing it directly caused ImportError (#1784)
def parse_bool(expr: Expression) -> bool | None:
    if isinstance(expr, NameExpr):
        if expr.fullname == "builtins.True":
            return True
        if expr.fullname == "builtins.False":
            return False
    return None


def get_literal_str_type(typ: Type) -> str | None:
    """Extract the str value of a string like type if possible"""
    typ = get_proper_type(typ)
    if (isinstance(typ, LiteralType) and isinstance((literal_value := typ.value), str)) or (
        isinstance(typ, Instance)
        and isinstance(typ.last_known_value, LiteralType)
        and isinstance((literal_value := typ.last_known_value.value), str)
    ):
        return literal_value
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
            descriptor_type = make_optional_type(descriptor_type)
        return descriptor_type
    return AnyType(TypeOfAny.explicit)


def get_field_lookup_exact_type(api: TypeChecker, field: "Field[Any, Any]") -> MypyType:
    if isinstance(field, RelatedField | ForeignObjectRel):
        # Not using field.related_model because that may have str value "self"
        lookup_type_class = field.remote_field.model
        rel_model_info = lookup_class_typeinfo(api, lookup_type_class)
        if rel_model_info is None:
            return AnyType(TypeOfAny.from_error)
        return make_optional_type(Instance(rel_model_info, []))

    field_info = lookup_class_typeinfo(api, field.__class__)
    if field_info is None:
        return AnyType(TypeOfAny.explicit)
    return get_private_descriptor_type(field_info, "_pyi_lookup_exact_type", is_nullable=field.null)


def get_nested_meta_node_for_current_class(info: TypeInfo) -> TypeInfo | None:
    metaclass_sym = info.names.get("Meta")
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def create_type_info(name: str, module: str, bases: list[Instance]) -> TypeInfo:
    # make new class expression
    classdef = ClassDef(name, Block([]))
    classdef.fullname = module + "." + name

    # make new TypeInfo
    new_typeinfo = TypeInfo(SymbolTable(), classdef, module)
    new_typeinfo.bases = bases
    calculate_mro(new_typeinfo)
    new_typeinfo.metaclass_type = new_typeinfo.calculate_metaclass_type()

    classdef.info = new_typeinfo

    return new_typeinfo


def add_new_class_for_module(
    module: MypyFile,
    name: str,
    bases: list[Instance],
    fields: dict[str, MypyType] | None = None,
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
    """
    Scope is guaranteed to be initialized with the module as the first element of the stack.
    Inspired from https://github.com/python/mypy/blob/15b8ca967cc6187effcab23e6613da2db4546584/mypy/checker.py#L5788
    """
    current_module = api.scope.stack[0]
    assert isinstance(current_module, MypyFile)
    return current_module


def make_oneoff_named_tuple(
    api: TypeChecker, name: str, fields: "dict[str, MypyType]", extra_bases: list[Instance] | None = None
) -> TupleType:
    current_module = get_current_module(api)
    if extra_bases is None:
        extra_bases = []
    namedtuple_info = add_new_class_for_module(
        current_module, name, bases=[api.named_generic_type("typing.NamedTuple", []), *extra_bases], fields=fields
    )
    return TupleType(list(fields.values()), fallback=Instance(namedtuple_info, []))


def make_tuple(api: "TypeChecker", fields: list[MypyType]) -> TupleType:
    # fallback for tuples is any builtins.tuple instance
    fallback = api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.special_form)])
    return TupleType(fields, fallback=fallback)


def convert_any_to_type(typ: MypyType, referred_to_type: MypyType) -> MypyType:
    proper_type = get_proper_type(typ)
    if isinstance(proper_type, UnionType):
        converted_items = []
        for item in proper_type.items:
            converted_items.append(convert_any_to_type(item, referred_to_type))
        return UnionType.make_union(converted_items, line=typ.line, column=typ.column)
    if isinstance(proper_type, Instance):
        args = []
        for default_arg in proper_type.args:
            default_arg = get_proper_type(default_arg)
            if isinstance(default_arg, AnyType):
                args.append(referred_to_type)
            else:
                args.append(default_arg)
        return proper_type.copy_modified(args=args)

    if isinstance(proper_type, AnyType):
        return referred_to_type

    return typ


def make_typeddict(
    api: SemanticAnalyzer | CheckerPluginInterface,
    fields: dict[str, MypyType],
    required_keys: set[str],
    readonly_keys: set[str],
) -> TypedDictType:
    if isinstance(api, CheckerPluginInterface):
        fallback_type = api.named_generic_type("typing._TypedDict", [])
    else:
        fallback_type = api.named_type("typing._TypedDict", [])
    return TypedDictType(
        fields,
        required_keys=required_keys,
        readonly_keys=readonly_keys,
        fallback=fallback_type,
    )


def resolve_string_attribute_value(attr_expr: Expression, django_context: "DjangoContext") -> str | None:
    if isinstance(attr_expr, StrExpr):
        return attr_expr.value

    if isinstance(attr_expr, NameExpr) and isinstance(attr_expr.node, Var) and attr_expr.node.type is not None:
        return get_literal_str_type(attr_expr.node.type)

    # support extracting from settings, in general case it's unresolvable yet
    if isinstance(attr_expr, MemberExpr):
        member_name = attr_expr.name
        if isinstance(attr_expr.expr, NameExpr) and attr_expr.expr.fullname == "django.conf.settings":
            if hasattr(django_context.settings, member_name):
                return getattr(django_context.settings, member_name)  # type: ignore[no-any-return]
    return None


def get_semanal_api(ctx: ClassDefContext | DynamicClassDefContext) -> SemanticAnalyzer:
    if not isinstance(ctx.api, SemanticAnalyzer):
        raise ValueError("Not a SemanticAnalyzer")
    return ctx.api


def get_typechecker_api(ctx: AttributeContext | MethodContext | FunctionContext) -> TypeChecker:
    if not isinstance(ctx.api, TypeChecker):
        raise ValueError("Not a TypeChecker")
    return ctx.api


def check_types_compatible(
    ctx: FunctionContext | MethodContext, *, expected_type: MypyType, actual_type: MypyType, error_message: str
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


def is_abstract_model(model: TypeInfo) -> bool:
    if model.fullname in fullnames.DJANGO_ABSTRACT_MODELS:
        return True

    if not is_model_type(model):
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
                stmt_type = get_proper_type(stmt.type)
                is_literal_true = isinstance(stmt_type, LiteralType) and stmt_type.value is True
                metadata["is_abstract_model"] = rhs_is_true or is_literal_true
                return metadata["is_abstract_model"]

    metadata["is_abstract_model"] = False
    return False


def resolve_lazy_reference(
    reference: str, *, api: TypeChecker | SemanticAnalyzer, django_context: "DjangoContext", ctx: Context
) -> TypeInfo | None:
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
        if isinstance(api, SemanticAnalyzer) and not api.final_iteration:
            # Getting this far, where Django matched the reference but we still can't
            # find it, we want to defer
            api.defer()
    else:
        api.fail("Could not match lazy reference with any model", ctx)
    return None


def is_model_type(info: TypeInfo) -> bool:
    return info.metaclass_type is not None and info.metaclass_type.type.has_base(fullnames.MODEL_METACLASS_FULLNAME)


def get_model_from_expression(
    expr: Expression,
    *,
    self_model: TypeInfo,
    api: TypeChecker | SemanticAnalyzer,
    django_context: "DjangoContext",
) -> Instance | None:
    """
    Attempts to resolve an expression to a 'TypeInfo' instance. Any lazy reference
    argument(e.g. "<app_label>.<object_name>") to a Django model is also attempted.
    """
    if isinstance(expr, RefExpr) and isinstance(expr.node, TypeInfo):
        if is_model_type(expr.node):
            return Instance(expr.node, [])

    if isinstance(expr, StrExpr) and expr.value == "self":
        return Instance(self_model, [])

    lazy_reference = None
    if isinstance(expr, StrExpr):
        lazy_reference = expr.value
    elif (
        isinstance(expr, MemberExpr)
        and isinstance(expr.expr, NameExpr)
        and f"{expr.expr.fullname}.{expr.name}" == fullnames.AUTH_USER_MODEL_FULLNAME
    ):
        lazy_reference = django_context.settings.AUTH_USER_MODEL

    if lazy_reference is not None:
        model_info = resolve_lazy_reference(lazy_reference, api=api, django_context=django_context, ctx=expr)
        if model_info is not None:
            return Instance(model_info, [])
    return None


def fill_manager(manager: TypeInfo, typ: MypyType) -> Instance:
    return Instance(manager, [typ] if manager.is_generic() else [])


def merge_extra_attrs(
    base_extra_attrs: ExtraAttrs | None,
    *,
    new_attrs: dict[str, MypyType] | None = None,
    new_immutable: set[str] | None = None,
) -> ExtraAttrs:
    """
    Create a new `ExtraAttrs` by merging new attributes/immutable fields into a base.

    If base_extra_attrs is None, creates a fresh ExtraAttrs with only the new values.
    """
    if base_extra_attrs:
        return ExtraAttrs(
            attrs={**base_extra_attrs.attrs, **new_attrs} if new_attrs is not None else base_extra_attrs.attrs.copy(),
            immutable=(
                base_extra_attrs.immutable | new_immutable
                if new_immutable is not None
                else base_extra_attrs.immutable.copy()
            ),
            mod_name=None,
        )
    return ExtraAttrs(
        attrs=new_attrs or {},
        immutable=new_immutable,
        mod_name=None,
    )
