from typing import Optional

from mypy.checkmember import bind_self, is_final_node, type_object_type
from mypy.nodes import TypeInfo, Context, SymbolTableNode, FuncBase
from mypy.subtypes import is_subtype, is_equivalent
from mypy.types import FunctionLike, CallableType, Type


def make_inner_classes_with_inherit_from_any_compatible_with_each_other():
    from mypy.checker import TypeChecker

    def determine_type_of_class_member(self, sym: SymbolTableNode) -> Optional[Type]:
        if sym.type is not None:
            return sym.type
        if isinstance(sym.node, FuncBase):
            return self.function_type(sym.node)
        if isinstance(sym.node, TypeInfo):
            # nested class
            return type_object_type(sym.node, self.named_type)
        return None

    TypeChecker.determine_type_of_class_member = determine_type_of_class_member

    def check_compatibility(self, name: str, base1: TypeInfo,
                            base2: TypeInfo, ctx: Context) -> None:
        """Check if attribute name in base1 is compatible with base2 in multiple inheritance.
        Assume base1 comes before base2 in the MRO, and that base1 and base2 don't have
        a direct subclass relationship (i.e., the compatibility requirement only derives from
        multiple inheritance).
        """
        if name in ('__init__', '__new__', '__init_subclass__'):
            # __init__ and friends can be incompatible -- it's a special case.
            return
        first = base1[name]
        second = base2[name]
        first_type = self.determine_type_of_class_member(first)
        second_type = self.determine_type_of_class_member(second)

        # TODO: What if some classes are generic?
        if (isinstance(first_type, FunctionLike) and
                isinstance(second_type, FunctionLike)):
            if ((isinstance(first_type, CallableType)
                 and first_type.fallback.type.fullname() == 'builtins.type')
                    and (isinstance(second_type, CallableType)
                         and second_type.fallback.type.fullname() == 'builtins.type')):
                # Both members are classes (not necessary nested), check if compatible
                ok = is_subtype(first_type.ret_type, second_type.ret_type)
            else:
                # Method override
                first_sig = bind_self(first_type)
                second_sig = bind_self(second_type)
                ok = is_subtype(first_sig, second_sig, ignore_pos_arg_names=True)
        elif first_type and second_type:
            ok = is_equivalent(first_type, second_type)
        else:
            if first_type is None:
                self.msg.cannot_determine_type_in_base(name, base1.name(), ctx)
            if second_type is None:
                self.msg.cannot_determine_type_in_base(name, base2.name(), ctx)
            ok = True
        # Final attributes can never be overridden, but can override
        # non-final read-only attributes.
        if is_final_node(second.node):
            self.msg.cant_override_final(name, base2.name(), ctx)
        if is_final_node(first.node):
            self.check_no_writable(name, second.node, ctx)
        # __slots__ is special and the type can vary across class hierarchy.
        if name == '__slots__':
            ok = True
        if not ok:
            self.msg.base_class_definitions_incompatible(name, base1, base2,
                                                         ctx)

    TypeChecker.check_compatibility = check_compatibility
