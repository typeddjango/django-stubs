from abc import abstractmethod
from typing import (
    TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union,
    cast)

from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    Block, ClassDef, Expression, MemberExpr, MypyFile, NameExpr, StrExpr, SymbolTable, SymbolTableNode,
    TypeInfo, Var,
    CallExpr, Context, PlaceholderNode, FuncDef, FakeInfo, OverloadedFuncDef, Decorator)
from mypy.plugin import DynamicClassDefContext, ClassDefContext, AttributeContext, MethodContext
from mypy.plugins.common import add_method
from mypy.semanal import SemanticAnalyzer, is_valid_replacement, is_same_symbol
from mypy.types import AnyType, Instance, NoneTyp, TypeType, ProperType, CallableType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, UnionType
from mypy.typetraverser import TypeTraverserVisitor

from django.db.models.fields import Field
from mypy_django_plugin.lib import fullnames
from mypy_django_plugin.lib.sem_helpers import prepare_unannotated_method_signature, analyze_callable_signature
from mypy_django_plugin.transformers2 import new_helpers

if TYPE_CHECKING:
    from mypy_django_plugin.django.context import DjangoContext
    from mypy_django_plugin.main import NewSemanalDjangoPlugin

AnyPluginAPI = Union[TypeChecker, SemanticAnalyzer]


class DjangoPluginCallback:
    django_context: 'DjangoContext'

    def __init__(self, plugin: 'NewSemanalDjangoPlugin') -> None:
        self.plugin = plugin
        self.django_context = plugin.django_context

    def new_typeinfo(self, name: str, bases: List[Instance]) -> TypeInfo:
        class_def = ClassDef(name, Block([]))
        class_def.fullname = self.qualified_name(name)

        info = TypeInfo(SymbolTable(), class_def, self.get_current_module().fullname)
        info.bases = bases
        calculate_mro(info)
        info.metaclass_type = info.calculate_metaclass_type()

        class_def.info = info
        return info

    @abstractmethod
    def get_current_module(self) -> MypyFile:
        raise NotImplementedError()

    @abstractmethod
    def qualified_name(self, name: str) -> str:
        raise NotImplementedError()


class SemanalPluginCallback(DjangoPluginCallback):
    semanal_api: SemanticAnalyzer

    def build_defer_error_message(self, message: str) -> str:
        return f'{self.__class__.__name__}: {message}'

    def defer_till_next_iteration(self, deferral_context: Optional[Context] = None,
                                  *,
                                  reason: Optional[str] = None) -> bool:
        """ Returns False if cannot be deferred. """
        if self.semanal_api.final_iteration:
            return False
        self.semanal_api.defer(deferral_context)
        # when pytest-mypy-plugins changes to incorporate verbose mypy logging,
        # uncomment following line to allow better feedback from users on issues
        # print(f'LOG: defer: {self.build_defer_error_message(reason)}')
        return True

    def get_current_module(self) -> MypyFile:
        return self.semanal_api.cur_mod_node

    def qualified_name(self, name: str) -> str:
        return self.semanal_api.qualified_name(name)

    def lookup_typeinfo_or_defer(self, fullname: str, *,
                                 deferral_context: Optional[Context] = None,
                                 reason_for_defer: Optional[str] = None) -> Optional[TypeInfo]:
        sym = self.plugin.lookup_fully_qualified(fullname)
        if sym is None or sym.node is None or isinstance(sym.node, PlaceholderNode):
            deferral_context = deferral_context or self.semanal_api.cur_mod_node
            reason = reason_for_defer or f'{fullname!r} is not available for lookup'
            if not self.defer_till_next_iteration(deferral_context, reason=reason):
                raise new_helpers.TypeInfoNotFound(fullname)
            return None

        if not isinstance(sym.node, TypeInfo):
            raise ValueError(f'{fullname!r} does not correspond to TypeInfo')

        return sym.node

    def new_typeinfo(self, name: str, bases: List[Instance], module_fullname: Optional[str] = None) -> TypeInfo:
        class_def = ClassDef(name, Block([]))
        class_def.fullname = self.semanal_api.qualified_name(name)

        info = TypeInfo(SymbolTable(), class_def,
                        module_fullname or self.get_current_module().fullname)
        info.bases = bases
        calculate_mro(info)
        info.metaclass_type = info.calculate_metaclass_type()

        class_def.info = info
        return info

    def add_symbol_table_node(self,
                              name: str,
                              symbol: SymbolTableNode,
                              symbol_table: Optional[SymbolTable] = None,
                              context: Optional[Context] = None,
                              can_defer: bool = True,
                              escape_comprehensions: bool = False) -> None:
        """ Patched copy of SemanticAnalyzer.add_symbol_table_node(). """
        names = symbol_table or self.semanal_api.current_symbol_table(escape_comprehensions=escape_comprehensions)
        existing = names.get(name)
        if isinstance(symbol.node, PlaceholderNode) and can_defer:
            self.semanal_api.defer(context)
            return None
        if (existing is not None
                and context is not None
                and not is_valid_replacement(existing, symbol)):
            # There is an existing node, so this may be a redefinition.
            # If the new node points to the same node as the old one,
            # or if both old and new nodes are placeholders, we don't
            # need to do anything.
            old = existing.node
            new = symbol.node
            if isinstance(new, PlaceholderNode):
                # We don't know whether this is okay. Let's wait until the next iteration.
                return False
            if not is_same_symbol(old, new):
                if isinstance(new, (FuncDef, Decorator, OverloadedFuncDef, TypeInfo)):
                    self.semanal_api.add_redefinition(names, name, symbol)
                if not (isinstance(new, (FuncDef, Decorator))
                        and self.semanal_api.set_original_def(old, new)):
                    self.semanal_api.name_already_defined(name, context, existing)
        elif name not in self.semanal_api.missing_names and '*' not in self.semanal_api.missing_names:
            names[name] = symbol
            self.progress = True
            return None
        raise new_helpers.SymbolAdditionNotPossible()

    # def add_symbol_table_node_or_defer(self, name: str, sym: SymbolTableNode) -> bool:
    #     return self.semanal_api.add_symbol_table_node(name, sym,
    #                                                   context=self.semanal_api.cur_mod_node)

    def add_method_from_signature(self,
                                  signature_node: FuncDef,
                                  new_method_name: str,
                                  new_self_type: Instance,
                                  class_defn: ClassDef) -> bool:
        if signature_node.type is None:
            if self.defer_till_next_iteration(reason=signature_node.fullname):
                return False

            arguments, return_type = prepare_unannotated_method_signature(signature_node)
            ctx = ClassDefContext(class_defn, signature_node, self.semanal_api)
            add_method(ctx,
                       new_method_name,
                       self_type=new_self_type,
                       args=arguments,
                       return_type=return_type)
            return True

        # add imported objects from method signature to the current module, if not present
        source_symbols = self.semanal_api.modules[signature_node.info.module_name].names
        currently_imported_symbols = self.semanal_api.cur_mod_node.names

        def import_symbol_from_source(name: str) -> None:
            if name in source_symbols['__builtins__'].node.names:
                return
            sym = source_symbols[name].copy()
            self.semanal_api.add_imported_symbol(name, sym, context=self.semanal_api.cur_mod_node)

        class UnimportedTypesVisitor(TypeTraverserVisitor):
            def visit_instance(self, t: Instance) -> None:
                super().visit_instance(t)
                if isinstance(t.type, FakeInfo):
                    return
                type_name = t.type.name
                sym = currently_imported_symbols.get(type_name)
                if sym is None:
                    import_symbol_from_source(type_name)

        signature_node.type.accept(UnimportedTypesVisitor())

        # # copy global SymbolTableNode objects from original class to the current node, if not present
        # original_module = semanal_api.modules[method_node.info.module_name]
        # for name, sym in original_module.names.items():
        #     if (not sym.plugin_generated
        #             and name not in semanal_api.cur_mod_node.names):
        #         semanal_api.add_imported_symbol(name, sym, context=semanal_api.cur_mod_node)

        arguments, analyzed_return_type, unbound = analyze_callable_signature(self.semanal_api, signature_node)
        if unbound:
            raise new_helpers.IncompleteDefnError(f'Signature of method {signature_node.fullname!r} is not ready')

        assert len(arguments) + 1 == len(signature_node.arguments)
        assert analyzed_return_type is not None

        ctx = ClassDefContext(class_defn, signature_node, self.semanal_api)
        add_method(ctx,
                   new_method_name,
                   self_type=new_self_type,
                   args=arguments,
                   return_type=analyzed_return_type)
        return True


class DynamicClassPluginCallback(SemanalPluginCallback):
    class_name: str
    call_expr: CallExpr

    def __call__(self, ctx: DynamicClassDefContext) -> None:
        self.class_name = ctx.name
        self.call_expr = ctx.call
        self.semanal_api = cast(SemanticAnalyzer, ctx.api)
        self.create_new_dynamic_class()

    def get_callee(self) -> MemberExpr:
        callee = self.call_expr.callee
        assert isinstance(callee, MemberExpr)
        return callee

    def lookup_same_module_or_defer(self, name: str, *,
                                    deferral_context: Optional[Context] = None) -> Optional[SymbolTableNode]:
        sym = self.semanal_api.lookup_qualified(name, self.call_expr)
        if sym is None or sym.node is None or isinstance(sym.node, PlaceholderNode):
            deferral_context = deferral_context or self.call_expr
            if not self.defer_till_next_iteration(deferral_context,
                                                  reason=f'{self.semanal_api.cur_mod_id}.{name} does not exist'):
                raise new_helpers.NameNotFound(name)
            return None
        return sym

    @abstractmethod
    def create_new_dynamic_class(self) -> None:
        raise NotImplementedError


class ClassDefPluginCallback(SemanalPluginCallback):
    reason: Expression
    class_defn: ClassDef
    ctx: ClassDefContext

    def __call__(self, ctx: ClassDefContext) -> None:
        self.reason = ctx.reason
        self.class_defn = ctx.cls
        self.semanal_api = cast(SemanticAnalyzer, ctx.api)
        self.ctx = ctx
        self.modify_class_defn()

    @abstractmethod
    def modify_class_defn(self) -> None:
        raise NotImplementedError


class TypeCheckerPluginCallback(DjangoPluginCallback):
    type_checker: TypeChecker

    def get_current_module(self) -> MypyFile:
        current_module = None
        for item in reversed(self.type_checker.scope.stack):
            if isinstance(item, MypyFile):
                current_module = item
                break
        assert current_module is not None
        return current_module

    def qualified_name(self, name: str) -> str:
        return self.type_checker.scope.stack[-1].fullname + '.' + name

    def lookup_typeinfo(self, fullname: str) -> Optional[TypeInfo]:
        sym = self.plugin.lookup_fully_qualified(fullname)
        if sym is None or sym.node is None:
            return None
        if not isinstance(sym.node, TypeInfo):
            raise ValueError(f'{fullname!r} does not correspond to TypeInfo')
        return sym.node


class GetMethodPluginCallback(TypeCheckerPluginCallback):
    callee_type: Instance
    ctx: MethodContext

    def __call__(self, ctx: MethodContext) -> MypyType:
        self.type_checker = ctx.api

        assert isinstance(ctx.type, CallableType)
        self.callee_type = ctx.type.ret_type
        self.ctx = ctx
        return self.get_method_return_type()

    @abstractmethod
    def get_method_return_type(self) -> MypyType:
        raise NotImplementedError


class GetAttributeCallback(TypeCheckerPluginCallback):
    obj_type: ProperType
    default_attr_type: MypyType
    error_context: MemberExpr
    name: str

    def __call__(self, ctx: AttributeContext) -> MypyType:
        self.ctx = ctx
        self.type_checker = ctx.api
        self.obj_type = ctx.type
        self.default_attr_type = ctx.default_attr_type
        self.error_context = ctx.context
        assert isinstance(self.error_context, MemberExpr)
        self.name = self.error_context.name
        return self.default_attr_type


def get_django_metadata(model_info: TypeInfo) -> Dict[str, Any]:
    return model_info.metadata.setdefault('django', {})


def split_symbol_name(fullname: str, all_modules: Dict[str, MypyFile]) -> Optional[Tuple[str, str]]:
    if '.' not in fullname:
        return None
    module_name = None
    parts = fullname.split('.')
    for i in range(len(parts), 0, -1):
        possible_module_name = '.'.join(parts[:i])
        if possible_module_name in all_modules:
            module_name = possible_module_name
            break
    if module_name is None:
        return None

    symbol_name = fullname.replace(module_name, '').lstrip('.')
    return module_name, symbol_name


def lookup_fully_qualified_typeinfo(api: AnyPluginAPI, fullname: str) -> Optional[TypeInfo]:
    split = split_symbol_name(fullname, api.modules)
    if split is None:
        return None
    module_name, cls_name = split

    sym_table = api.modules[module_name].names  # type: Dict[str, SymbolTableNode]
    if '.' in cls_name:
        parent_cls_name, _, cls_name = cls_name.rpartition('.')
        # nested class
        for parent_cls_name in parent_cls_name.split('.'):
            sym = sym_table.get(parent_cls_name)
            if (sym is None or sym.node is None
                    or not isinstance(sym.node, TypeInfo)):
                return None
            sym_table = sym.node.names

    sym = sym_table.get(cls_name)
    if (sym is None
            or sym.node is None
            or not isinstance(sym.node, TypeInfo)):
        return None
    return sym.node


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
