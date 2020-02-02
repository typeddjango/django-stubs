from typing import Optional

from mypy.checker import gen_unique_name
from mypy.nodes import NameExpr, TypeInfo, SymbolTableNode, StrExpr
from mypy.types import Type as MypyType, TypeVarType, TypeVarDef, Instance

from mypy_django_plugin.lib import helpers, fullnames, chk_helpers, sem_helpers
from mypy_django_plugin.transformers.managers import iter_all_custom_queryset_methods


class CreateNewManagerClassFrom_FromQuerySet(helpers.DynamicClassPluginCallback):
    def create_typevar_in_current_module(self, name: str,
                                         upper_bound: Optional[MypyType] = None) -> TypeVarDef:
        tvar_name = gen_unique_name(name, self.semanal_api.globals)
        tvar_def = TypeVarDef(tvar_name,
                              fullname=self.semanal_api.cur_mod_id + '.' + tvar_name,
                              id=-1,
                              values=[],
                              upper_bound=upper_bound)
        return tvar_def

    def create_new_dynamic_class(self) -> None:
        # extract Manager class which will act as base
        callee = self.get_callee()
        fullname = callee.fullname or callee.expr.fullname
        callee_manager_info = self.lookup_typeinfo_or_defer(fullname)
        if callee_manager_info is None:
            return None

        # extract queryset from which we're going to copy methods
        passed_queryset_name_expr = self.call_expr.args[0]
        assert isinstance(passed_queryset_name_expr, NameExpr)
        queryset_class_name = passed_queryset_name_expr.name
        sym = self.lookup_same_module_or_defer(queryset_class_name)
        if sym is None:
            return None
        assert isinstance(sym.node, TypeInfo)
        passed_queryset_info = sym.node

        # for TypeVar bound
        base_model_info = self.lookup_typeinfo_or_defer(fullnames.MODEL_CLASS_FULLNAME)
        if base_model_info is None:
            return
        model_tvar_defn = self.create_typevar_in_current_module('_M', upper_bound=Instance(base_model_info, []))
        model_tvar_type = TypeVarType(model_tvar_defn)

        # make Manager[_T]
        parent_manager_type = Instance(callee_manager_info, [model_tvar_type])

        # instantiate with a proper model, Manager[MyModel], filling all Manager type vars in process
        new_manager_info = self.new_typeinfo(self.class_name,
                                             bases=[parent_manager_type])
        new_manager_info.defn.type_vars = [model_tvar_defn]
        new_manager_info.type_vars = [model_tvar_defn.name]
        new_manager_info.set_line(self.call_expr)

        # copy methods from passed_queryset_info with self type replaced
        self_type = Instance(new_manager_info, [model_tvar_type])
        for name, method_node in iter_all_custom_queryset_methods(passed_queryset_info):
            self.add_method_from_signature(method_node,
                                           name,
                                           self_type,
                                           new_manager_info.defn)

        new_manager_sym = SymbolTableNode(self.semanal_api.current_symbol_kind(),
                                          new_manager_info,
                                          plugin_generated=True)
        self.semanal_api.add_symbol_table_node(self.class_name, new_manager_sym)

        # add mapping between generated manager and current one
        runtime_manager_class_name = None
        if 'class_name' in self.call_expr.arg_names:
            class_name_arg = self.call_expr.args[self.call_expr.arg_names.index('class_name')]
            if isinstance(class_name_arg, StrExpr):
                runtime_manager_class_name = class_name_arg.value

        new_manager_name = runtime_manager_class_name or (callee_manager_info.name + 'From' + queryset_class_name)
        django_generated_manager_name = 'django.db.models.manager.' + new_manager_name
        base_model_info.metadata.setdefault('managers', {})[django_generated_manager_name] = new_manager_info.fullname
