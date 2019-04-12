from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Tuple, cast

import dataclasses
from mypy.nodes import (
    ARG_POS, ARG_STAR, ARG_STAR2, MDEF, Argument, CallExpr, ClassDef, Expression, IndexExpr, MemberExpr, MypyFile,
    NameExpr, StrExpr, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import ClassDefContext
from mypy.plugins.common import add_method
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import AnyType, Instance, NoneTyp, TypeOfAny

from mypy_django_plugin import helpers


@dataclasses.dataclass
class ModelClassInitializer(metaclass=ABCMeta):
    api: SemanticAnalyzerPass2
    model_classdef: ClassDef

    @classmethod
    def from_ctx(cls, ctx: ClassDefContext):
        return cls(api=cast(SemanticAnalyzerPass2, ctx.api), model_classdef=ctx.cls)

    def get_meta_attribute(self, name: str) -> Optional[Expression]:
        meta_node = helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None

        return helpers.get_assigned_value_for_class(meta_node, name)

    def is_abstract_model(self) -> bool:
        is_abstract_expr = self.get_meta_attribute('abstract')
        if is_abstract_expr is None:
            return False
        return self.api.parse_bool(is_abstract_expr)

    def add_new_node_to_model_class(self, name: str, typ: Instance) -> None:
        # type=: type of the variable itself
        var = Var(name=name, type=typ)
        # var.info: type of the object variable is bound to
        var.info = self.model_classdef.info
        var._fullname = self.model_classdef.info.fullname() + '.' + name
        var.is_inferred = True
        var.is_initialized_in_class = True
        self.model_classdef.info.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True)

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()


def iter_over_one_to_n_related_fields(klass: ClassDef) -> Iterator[Tuple[NameExpr, CallExpr]]:
    for lvalue, rvalue in helpers.iter_call_assignments(klass):
        if (isinstance(lvalue, NameExpr)
                and isinstance(rvalue.callee, MemberExpr)):
            if rvalue.callee.fullname in {helpers.FOREIGN_KEY_FULLNAME,
                                          helpers.ONETOONE_FIELD_FULLNAME}:
                yield lvalue, rvalue


class SetIdAttrsForRelatedFields(ModelClassInitializer):
    def run(self) -> None:
        for lvalue, rvalue in iter_over_one_to_n_related_fields(self.model_classdef):
            node_name = lvalue.name + '_id'
            self.add_new_node_to_model_class(name=node_name,
                                             typ=self.api.builtin_type('builtins.int'))


class InjectAnyAsBaseForNestedMeta(ModelClassInitializer):
    def run(self) -> None:
        meta_node = helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddDefaultObjectsManager(ModelClassInitializer):
    def add_new_manager(self, name: str, manager_type: Optional[Instance]) -> None:
        if manager_type is None:
            return None
        self.add_new_node_to_model_class(name, manager_type)

    def add_private_default_manager(self, manager_type: Optional[Instance]) -> None:
        if manager_type is None:
            return None
        self.add_new_node_to_model_class('_default_manager', manager_type)

    def get_existing_managers(self) -> List[Tuple[str, TypeInfo]]:
        managers = []
        for base in self.model_classdef.info.mro:
            for name_expr, member_expr in helpers.iter_call_assignments(base.defn):
                manager_name = name_expr.name
                callee_expr = member_expr.callee
                if isinstance(callee_expr, IndexExpr):
                    callee_expr = callee_expr.analyzed.expr
                if isinstance(callee_expr, (MemberExpr, NameExpr)) \
                        and isinstance(callee_expr.node, TypeInfo) \
                        and callee_expr.node.has_base(helpers.BASE_MANAGER_CLASS_FULLNAME):
                    managers.append((manager_name, callee_expr.node))
        return managers

    def run(self) -> None:
        existing_managers = self.get_existing_managers()
        if existing_managers:
            first_manager_type = None
            for manager_name, manager_type_info in existing_managers:
                manager_type = Instance(manager_type_info, args=[Instance(self.model_classdef.info, [])])
                self.add_new_manager(name=manager_name, manager_type=manager_type)
                if first_manager_type is None:
                    first_manager_type = manager_type
        else:
            if self.is_abstract_model():
                # abstract models do not need 'objects' queryset
                return None

            first_manager_type = self.api.named_type_or_none(helpers.MANAGER_CLASS_FULLNAME,
                                                             args=[Instance(self.model_classdef.info, [])])
            self.add_new_manager('objects', manager_type=first_manager_type)

        if self.is_abstract_model():
            return None
        default_manager_name_expr = self.get_meta_attribute('default_manager_name')
        if isinstance(default_manager_name_expr, StrExpr):
            self.add_private_default_manager(self.model_classdef.info.get(default_manager_name_expr.value).type)
        else:
            self.add_private_default_manager(first_manager_type)


class AddIdAttributeIfPrimaryKeyTrueIsNotSet(ModelClassInitializer):
    def run(self) -> None:
        if self.is_abstract_model():
            # no need for .id attr
            return None

        for _, rvalue in helpers.iter_call_assignments(self.model_classdef):
            if ('primary_key' in rvalue.arg_names
                    and self.api.parse_bool(rvalue.args[rvalue.arg_names.index('primary_key')])):
                break
        else:
            self.add_new_node_to_model_class('id', self.api.builtin_type('builtins.object'))


class AddRelatedManagers(ModelClassInitializer):
    def add_related_manager_variable(self, manager_name: str, related_field_type_data: Dict[str, Any]) -> None:
        # add dummy related manager for use later
        self.add_new_node_to_model_class(manager_name, self.api.builtin_type('builtins.object'))

        # save name in metadata for use in get_attribute_hook later
        related_managers_metadata = helpers.get_related_managers_metadata(self.model_classdef.info)
        related_managers_metadata[manager_name] = related_field_type_data

    def run(self) -> None:
        for module_name, module_file in self.api.modules.items():
            for model_defn in helpers.iter_over_classdefs(module_file):
                for lvalue, rvalue in helpers.iter_call_assignments(model_defn):
                    if is_related_field(rvalue, module_file):
                        try:
                            referenced_model_fullname = extract_ref_to_fullname(rvalue,
                                                                                module_file=module_file,
                                                                                all_modules=self.api.modules)
                        except helpers.SelfReference:
                            referenced_model_fullname = model_defn.fullname

                        except helpers.SameFileModel as exc:
                            referenced_model_fullname = module_name + '.' + exc.model_cls_name

                        if self.model_classdef.fullname == referenced_model_fullname:
                            related_name = model_defn.name.lower() + '_set'
                            if 'related_name' in rvalue.arg_names:
                                related_name_expr = rvalue.args[rvalue.arg_names.index('related_name')]
                                if not isinstance(related_name_expr, StrExpr):
                                    continue
                                related_name = related_name_expr.value
                                if related_name == '+':
                                    # No backwards relation is desired
                                    continue

                            if 'related_query_name' in rvalue.arg_names:
                                related_query_name_expr = rvalue.args[rvalue.arg_names.index('related_query_name')]
                                if not isinstance(related_query_name_expr, StrExpr):
                                    related_query_name = None
                                else:
                                    related_query_name = related_query_name_expr.value
                                # TODO: Handle defaulting to model name if related_name is not set
                            else:
                                # No related_query_name specified, default to related_name
                                related_query_name = related_name

                            # field_type_data = get_related_field_type(rvalue, self.api, defn.info)
                            # if typ is None:
                            #     continue

                            # TODO: recursively serialize types, or just https://github.com/python/mypy/issues/6506
                            # as long as Model is not a Generic, one level depth is fine
                            if rvalue.callee.name in {'ForeignKey', 'ManyToManyField'}:
                                field_type_data = {
                                    'manager': helpers.RELATED_MANAGER_CLASS_FULLNAME,
                                    'of': [model_defn.info.fullname()]
                                }
                                # return api.named_type_or_none(helpers.RELATED_MANAGER_CLASS_FULLNAME,
                                #                               args=[Instance(related_model_typ, [])])
                            else:
                                field_type_data = {
                                    'manager': model_defn.info.fullname(),
                                    'of': []
                                }

                            self.add_related_manager_variable(related_name, related_field_type_data=field_type_data)

                            if related_query_name is not None:
                                # Only create related_query_name if it is a string literal
                                helpers.get_lookups_metadata(self.model_classdef.info)[related_query_name] = {
                                    'related_query_name_target': related_name
                                }


def get_related_field_type(rvalue: CallExpr, related_model_typ: TypeInfo) -> Dict[str, Any]:
    if rvalue.callee.name in {'ForeignKey', 'ManyToManyField'}:
        return {
            'manager': helpers.RELATED_MANAGER_CLASS_FULLNAME,
            'of': [related_model_typ.fullname()]
        }
        # return api.named_type_or_none(helpers.RELATED_MANAGER_CLASS_FULLNAME,
        #                               args=[Instance(related_model_typ, [])])
    else:
        return {
            'manager': related_model_typ.fullname(),
            'of': []
        }
        # return Instance(related_model_typ, [])


def is_related_field(expr: CallExpr, module_file: MypyFile) -> bool:
    if isinstance(expr.callee, MemberExpr) and isinstance(expr.callee.expr, NameExpr):
        module = module_file.names.get(expr.callee.expr.name)
        if module \
                and module.fullname == 'django.db.models' \
                and expr.callee.name in {'ForeignKey',
                                         'OneToOneField',
                                         'ManyToManyField'}:
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
        typ_fullname = helpers.get_model_fullname_from_string(to_expr.value, all_modules)
        if typ_fullname is None:
            return None
        return typ_fullname
    return None


def add_dummy_init_method(ctx: ClassDefContext) -> None:
    any = AnyType(TypeOfAny.special_form)

    pos_arg = Argument(variable=Var('args', any),
                       type_annotation=any, initializer=None, kind=ARG_STAR)
    kw_arg = Argument(variable=Var('kwargs', any),
                      type_annotation=any, initializer=None, kind=ARG_STAR2)

    add_method(ctx, '__init__', [pos_arg, kw_arg], NoneTyp())

    # mark as model class
    ctx.cls.info.metadata.setdefault('django', {})['generated_init'] = True


def add_get_set_attr_fallback_to_any(ctx: ClassDefContext):
    any = AnyType(TypeOfAny.special_form)

    name_arg = Argument(variable=Var('name', any),
                        type_annotation=any, initializer=None, kind=ARG_POS)
    add_method(ctx, '__getattr__', [name_arg], any)

    value_arg = Argument(variable=Var('value', any),
                         type_annotation=any, initializer=None, kind=ARG_POS)
    add_method(ctx, '__setattr__', [name_arg, value_arg], any)


def process_model_class(ctx: ClassDefContext, ignore_unknown_attributes: bool) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultObjectsManager,
        AddIdAttributeIfPrimaryKeyTrueIsNotSet,
        SetIdAttrsForRelatedFields,
        AddRelatedManagers,
    ]
    for initializer_cls in initializers:
        initializer_cls.from_ctx(ctx).run()

    add_dummy_init_method(ctx)

    if ignore_unknown_attributes:
        add_get_set_attr_fallback_to_any(ctx)
