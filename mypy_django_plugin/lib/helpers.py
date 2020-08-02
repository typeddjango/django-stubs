from abc import abstractmethod
from typing import (
    TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union, cast,
)

from mypy.checker import TypeChecker
from mypy.mro import calculate_mro
from mypy.nodes import (
    GDEF, Argument, Block, CallExpr, ClassDef, Context, Expression, FuncDef, MemberExpr, MypyFile, NameExpr,
    PlaceholderNode, StrExpr, SymbolTable, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import (
    AttributeContext, ClassDefContext, DynamicClassDefContext, FunctionContext, MethodContext,
)
from mypy.plugins.common import add_method_to_class
from mypy.semanal import SemanticAnalyzer
from mypy.types import AnyType, CallableType, Instance, NoneTyp, ProperType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, UnionType

from mypy_django_plugin.transformers import new_helpers

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

    def copy_method_to_another_class(
            self,
            ctx: ClassDefContext,
            self_type: Instance,
            new_method_name: str,
            method_node: FuncDef) -> None:
        if method_node.type is None:
            if not self.defer_till_next_iteration(reason='method_node.type is None'):
                raise new_helpers.TypeInfoNotFound(method_node.fullname)

            arguments, return_type = build_unannotated_method_args(method_node)
            add_method_to_class(
                ctx.api,
                ctx.cls,
                new_method_name,
                args=arguments,
                return_type=return_type,
                self_type=self_type)
            return

        method_type: CallableType = method_node.type
        if not isinstance(method_type, CallableType) and not self.defer_till_next_iteration(
                reason='method_node.type is not CallableType'):
            raise new_helpers.TypeInfoNotFound(method_node.fullname)

        arguments = []
        bound_return_type = self.semanal_api.anal_type(
            method_type.ret_type,
            allow_placeholder=True)

        assert bound_return_type is not None

        if isinstance(bound_return_type, PlaceholderNode):
            raise new_helpers.TypeInfoNotFound('return type ' + method_node.fullname)

        for arg_name, arg_type, original_argument in zip(
                method_type.arg_names[1:],
                method_type.arg_types[1:],
                method_node.arguments[1:]):
            bound_arg_type = self.semanal_api.anal_type(arg_type, allow_placeholder=True)
            if bound_arg_type is None and not self.defer_till_next_iteration(reason='bound_arg_type is None'):
                raise new_helpers.TypeInfoNotFound('of ' + arg_name + ' argument of ' + method_node.fullname)

            assert bound_arg_type is not None

            if isinstance(bound_arg_type, PlaceholderNode) and self.defer_till_next_iteration(
                    reason='bound_arg_type is None'):
                raise new_helpers.TypeInfoNotFound('of ' + arg_name + ' argument of ' + method_node.fullname)

            var = Var(
                name=original_argument.variable.name,
                type=arg_type)
            var.line = original_argument.variable.line
            var.column = original_argument.variable.column
            argument = Argument(
                variable=var,
                type_annotation=bound_arg_type,
                initializer=original_argument.initializer,
                kind=original_argument.kind)
            argument.set_line(original_argument)
            arguments.append(argument)

        add_method_to_class(
            ctx.api,
            ctx.cls,
            new_method_name,
            args=arguments,
            return_type=bound_return_type,
            self_type=self_type)

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


class DynamicClassPluginCallback(SemanalPluginCallback):
    class_name: str
    call_expr: CallExpr

    def __call__(self, ctx: DynamicClassDefContext) -> None:
        self.class_name = ctx.name
        self.call_expr = ctx.call
        self.semanal_api = cast(SemanticAnalyzer, ctx.api)
        self.create_new_dynamic_class()

    def generate_manager_info_and_module(self, base_manager_info: TypeInfo) -> Tuple[TypeInfo, MypyFile]:
        new_manager_info = self.semanal_api.basic_new_typeinfo(
            self.class_name,
            basetype_or_fallback=Instance(
                base_manager_info,
                [AnyType(TypeOfAny.unannotated)])
        )
        new_manager_info.line = self.call_expr.line
        new_manager_info.defn.line = self.call_expr.line
        new_manager_info.metaclass_type = new_manager_info.calculate_metaclass_type()

        current_module = self.semanal_api.cur_mod_node
        current_module.names[self.class_name] = SymbolTableNode(
            GDEF,
            new_manager_info,
            plugin_generated=True)
        return new_manager_info, current_module

    @abstractmethod
    def create_new_dynamic_class(self) -> None:
        raise NotImplementedError


class DynamicClassFromMethodCallback(DynamicClassPluginCallback):
    callee: MemberExpr

    def __call__(self, ctx: DynamicClassDefContext) -> None:
        self.class_name = ctx.name
        self.call_expr = ctx.call

        assert ctx.call.callee is not None
        if not isinstance(ctx.call.callee, MemberExpr):
            # throw error?
            return
        self.callee = ctx.call.callee

        self.semanal_api = cast(SemanticAnalyzer, ctx.api)
        self.create_new_dynamic_class()


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


class GetMethodCallback(TypeCheckerPluginCallback):
    ctx: MethodContext
    callee_type: Instance
    default_return_type: MypyType

    def __call__(self, ctx: MethodContext) -> MypyType:
        self.type_checker = cast(TypeChecker, ctx.api)
        self.ctx = ctx
        self.callee_type = cast(Instance, ctx.type)
        self.default_return_type = self.ctx.default_return_type
        return self.get_method_return_type()

    @abstractmethod
    def get_method_return_type(self) -> MypyType:
        raise NotImplementedError


class GetFunctionCallback(TypeCheckerPluginCallback):
    ctx: FunctionContext
    default_return_type: MypyType

    def __call__(self, ctx: FunctionContext) -> MypyType:
        self.type_checker = cast(TypeChecker, ctx.api)
        self.ctx = ctx
        self.default_return_type = ctx.default_return_type
        return self.get_function_return_type()

    @abstractmethod
    def get_function_return_type(self) -> MypyType:
        raise NotImplementedError


class GetAttributeCallback(TypeCheckerPluginCallback):
    obj_type: ProperType
    default_attr_type: MypyType
    error_context: MemberExpr
    name: str

    def __call__(self, ctx: AttributeContext) -> MypyType:
        self.ctx = ctx
        self.type_checker = cast(TypeChecker, ctx.api)
        self.obj_type = ctx.type
        self.default_attr_type = ctx.default_attr_type

        assert isinstance(ctx.context, MemberExpr)
        self.error_context = ctx.context
        self.name = ctx.context.name

        return self.get_attribute_type()

    @abstractmethod
    def get_attribute_type(self) -> MypyType:
        raise NotImplementedError()


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


def get_nested_meta_node_for_current_class(info: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = info.names.get('Meta')
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None


def build_unannotated_method_args(method_node: FuncDef) -> Tuple[List[Argument], MypyType]:
    prepared_arguments = []
    for argument in method_node.arguments[1:]:
        argument.type_annotation = AnyType(TypeOfAny.unannotated)
        prepared_arguments.append(argument)
    return_type = AnyType(TypeOfAny.unannotated)
    return prepared_arguments, return_type
