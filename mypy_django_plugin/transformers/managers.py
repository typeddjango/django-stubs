from typing import List, Tuple

from mypy.nodes import Argument, FuncDef, NameExpr, StrExpr, TypeInfo
from mypy.plugin import ClassDefContext
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import fullnames, helpers


def build_unannotated_method_args(method_node: FuncDef) -> Tuple[List[Argument], MypyType]:
    prepared_arguments = []
    for argument in method_node.arguments[1:]:
        argument.type_annotation = AnyType(TypeOfAny.unannotated)
        prepared_arguments.append(argument)
    return_type = AnyType(TypeOfAny.unannotated)
    return prepared_arguments, return_type


class ManagerFromQuerySetCallback(helpers.DynamicClassFromMethodCallback):
    def create_new_dynamic_class(self) -> None:

        base_manager_info = self.callee.expr.node  # type: ignore

        if base_manager_info is None and not self.defer_till_next_iteration(reason='base_manager_info is None'):
            # what exception should be thrown here?
            return

        assert isinstance(base_manager_info, TypeInfo)

        new_manager_info, current_module = self.generate_manager_info_and_module(base_manager_info)

        passed_queryset = self.call_expr.args[0]
        assert isinstance(passed_queryset, NameExpr)

        derived_queryset_fullname = passed_queryset.fullname
        assert derived_queryset_fullname is not None

        sym = self.semanal_api.lookup_fully_qualified_or_none(derived_queryset_fullname)
        assert sym is not None
        if sym.node is None and not self.defer_till_next_iteration(reason='sym.node is None'):
            # inherit from Any to prevent false-positives, if queryset class cannot be resolved
            new_manager_info.fallback_to_any = True
            return

        derived_queryset_info = sym.node
        assert isinstance(derived_queryset_info, TypeInfo)

        if len(self.call_expr.args) > 1:
            expr = self.call_expr.args[1]
            assert isinstance(expr, StrExpr)
            custom_manager_generated_name = expr.value
        else:
            custom_manager_generated_name = base_manager_info.name + 'From' + derived_queryset_info.name

        custom_manager_generated_fullname = '.'.join(['django.db.models.manager', custom_manager_generated_name])
        if 'from_queryset_managers' not in base_manager_info.metadata:
            base_manager_info.metadata['from_queryset_managers'] = {}
        base_manager_info.metadata['from_queryset_managers'][
            custom_manager_generated_fullname] = new_manager_info.fullname
        class_def_context = ClassDefContext(
            cls=new_manager_info.defn,
            reason=self.call_expr, api=self.semanal_api)
        self_type = Instance(new_manager_info, [])
        # we need to copy all methods in MRO before django.db.models.query.QuerySet
        for class_mro_info in derived_queryset_info.mro:
            if class_mro_info.fullname == fullnames.QUERYSET_CLASS_FULLNAME:
                break
            for name, sym in class_mro_info.names.items():
                if isinstance(sym.node, FuncDef):
                    self.copy_method_to_another_class(
                        class_def_context,
                        self_type,
                        new_method_name=name,
                        method_node=sym.node)
