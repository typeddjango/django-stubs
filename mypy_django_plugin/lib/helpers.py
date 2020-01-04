from typing import (
    TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Optional, Union,
)

from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    Block, ClassDef, Expression, MemberExpr, MypyFile, NameExpr, StrExpr, SymbolNode,
    SymbolTable, SymbolTableNode, TypeInfo, Var,
)
from mypy.semanal import SemanticAnalyzer
from mypy.types import AnyType, Instance, NoneTyp
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, UnionType

from django.db.models.fields import Field
from mypy_django_plugin.lib import fullnames

if TYPE_CHECKING:
    from mypy_django_plugin.django.context import DjangoContext

AnyPluginAPI = Union[TypeChecker, SemanticAnalyzer]


def get_django_metadata(model_info: TypeInfo) -> Dict[str, Any]:
    return model_info.metadata.setdefault('django', {})


def lookup_fully_qualified_sym(fullname: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolTableNode]:
    if '.' not in fullname:
        return None

    module_file = None
    parts = fullname.split('.')
    for i in range(len(parts), 0, -1):
        possible_module_name = '.'.join(parts[:i])
        if possible_module_name in all_modules:
            module_file = all_modules[possible_module_name]
            break

    if module_file is None:
        return None

    cls_name = fullname.replace(module_file.fullname, '').lstrip('.')
    sym_table = module_file.names
    if '.' in cls_name:
        parent_cls_name, _, cls_name = cls_name.rpartition('.')
        # nested class
        for parent_cls_name in parent_cls_name.split('.'):
            sym = sym_table.get(parent_cls_name)
            if sym is None:
                return None
            sym_table = sym.node.names

    return sym_table.get(cls_name)


def lookup_fully_qualified_generic(name: str, all_modules: Dict[str, MypyFile]) -> Optional[SymbolNode]:
    sym = lookup_fully_qualified_sym(name, all_modules)
    if sym is None:
        return None
    return sym.node


def lookup_fully_qualified_typeinfo(api: AnyPluginAPI, fullname: str) -> Optional[TypeInfo]:
    node = lookup_fully_qualified_generic(fullname, api.modules)
    if not isinstance(node, TypeInfo):
        return None
    return node


def lookup_class_typeinfo(api: AnyPluginAPI, klass: type) -> Optional[TypeInfo]:
    fullname = get_class_fullname(klass)
    field_info = lookup_fully_qualified_typeinfo(api, fullname)
    return field_info


def reparametrize_instance(instance: Instance, new_args: List[MypyType]) -> Instance:
    return Instance(instance.type, args=new_args,
                    line=instance.line, column=instance.column)


def get_class_fullname(klass: type) -> str:
    return klass.__module__ + '.' + klass.__qualname__


def make_optional(typ: MypyType) -> MypyType:
    return UnionType.make_union([typ, NoneTyp()])


def parse_bool(expr: Expression) -> Optional[bool]:
    if isinstance(expr, NameExpr):
        if expr.fullname == 'builtins.True':
            return True
        if expr.fullname == 'builtins.False':
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
    """ Return declared type of type_info's private_field_name (used for private Field attributes)"""
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


def get_field_lookup_exact_type(api: AnyPluginAPI, field: Field) -> MypyType:
    if isinstance(field, (RelatedField, ForeignObjectRel)):
        lookup_type_class = field.related_model
        rel_model_info = lookup_class_typeinfo(api, lookup_type_class)
        if rel_model_info is None:
            return AnyType(TypeOfAny.from_error)
        return make_optional(Instance(rel_model_info, []))

    field_info = lookup_class_typeinfo(api, field.__class__)
    if field_info is None:
        return AnyType(TypeOfAny.explicit)
    return get_private_descriptor_type(field_info, '_pyi_lookup_exact_type',
                                       is_nullable=field.null)


def get_current_module(api: AnyPluginAPI) -> MypyFile:
    if isinstance(api, SemanticAnalyzer):
        return api.cur_mod_node

    current_module = None
    for item in reversed(api.scope.stack):
        if isinstance(item, MypyFile):
            current_module = item
            break
    assert current_module is not None
    return current_module


def convert_any_to_type(typ: MypyType, referred_to_type: MypyType) -> MypyType:
    if isinstance(typ, UnionType):
        converted_items = []
        for item in typ.items:
            converted_items.append(convert_any_to_type(item, referred_to_type))
        return UnionType.make_union(converted_items,
                                    line=typ.line, column=typ.column)
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


def resolve_string_attribute_value(attr_expr: Expression, django_context: 'DjangoContext') -> Optional[str]:
    if isinstance(attr_expr, StrExpr):
        return attr_expr.value

    # support extracting from settings, in general case it's unresolvable yet
    if isinstance(attr_expr, MemberExpr):
        member_name = attr_expr.name
        if isinstance(attr_expr.expr, NameExpr) and attr_expr.expr.fullname == 'django.conf.settings':
            if hasattr(django_context.settings, member_name):
                return getattr(django_context.settings, member_name)
    return None


def is_subclass_of_model(info: TypeInfo, django_context: 'DjangoContext') -> bool:
    return (info.fullname in django_context.all_registered_model_class_fullnames
            or info.has_base(fullnames.MODEL_CLASS_FULLNAME))


def new_typeinfo(name: str,
                 *,
                 bases: List[Instance],
                 module_name: str) -> TypeInfo:
    """
        Construct new TypeInfo instance. Cannot be used for nested classes.
    """
    class_def = ClassDef(name, Block([]))
    class_def.fullname = module_name + '.' + name

    info = TypeInfo(SymbolTable(), class_def, module_name)
    info.bases = bases
    calculate_mro(info)
    info.metaclass_type = info.calculate_metaclass_type()

    class_def.info = info
    return info
