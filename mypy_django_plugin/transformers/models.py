from abc import ABCMeta, abstractmethod
from typing import Dict, Iterator, List, Optional, Tuple, cast

import dataclasses
from mypy.nodes import (
    ARG_STAR, ARG_STAR2, MDEF, Argument, CallExpr, ClassDef, Expression, IndexExpr, Lvalue, MemberExpr, MypyFile,
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
        var = Var(name=name, type=typ)
        var.info = typ.type
        var._fullname = self.model_classdef.info.fullname() + '.' + name
        var.is_inferred = True
        var.is_initialized_in_class = True
        self.model_classdef.info.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True)

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()


def iter_call_assignments(klass: ClassDef) -> Iterator[Tuple[Lvalue, CallExpr]]:
    for lvalue, rvalue in helpers.iter_over_assignments(klass):
        if isinstance(rvalue, CallExpr):
            yield lvalue, rvalue


def iter_over_one_to_n_related_fields(klass: ClassDef) -> Iterator[Tuple[NameExpr, CallExpr]]:
    for lvalue, rvalue in iter_call_assignments(klass):
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


def get_model_argument(manager_info: TypeInfo) -> Optional[Instance]:
    for base in manager_info.bases:
        if base.args:
            model_arg = base.args[0]
            if isinstance(model_arg, Instance) and model_arg.type.has_base(helpers.MODEL_CLASS_FULLNAME):
                return model_arg
    return None


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
            for name_expr, member_expr in iter_call_assignments(base.defn):
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

        for _, rvalue in iter_call_assignments(self.model_classdef):
            if ('primary_key' in rvalue.arg_names
                    and self.api.parse_bool(rvalue.args[rvalue.arg_names.index('primary_key')])):
                break
        else:
            self.add_new_node_to_model_class('id', self.api.builtin_type('builtins.object'))


class AddRelatedManagers(ModelClassInitializer):
    def run(self) -> None:
        for module_name, module_file in self.api.modules.items():
            for defn in iter_over_classdefs(module_file):
                for lvalue, rvalue in iter_call_assignments(defn):
                    if is_related_field(rvalue, module_file):
                        try:
                            ref_to_fullname = extract_ref_to_fullname(rvalue,
                                                                      module_file=module_file,
                                                                      all_modules=self.api.modules)
                        except helpers.SelfReference:
                            ref_to_fullname = defn.fullname

                        except helpers.SameFileModel as exc:
                            ref_to_fullname = module_name + '.' + exc.model_cls_name

                        if self.model_classdef.fullname == ref_to_fullname:
                            related_name = defn.name.lower() + '_set'
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
                            typ = get_related_field_type(rvalue, self.api, defn.info)
                            if typ is None:
                                continue
                            self.add_new_node_to_model_class(related_name, typ)
                            if related_query_name is not None:
                                # Only create related_query_name if it is a string literal
                                helpers.get_lookups_metadata(self.model_classdef.info)[related_query_name] = {
                                    'related_query_name_target': related_name
                                }


def iter_over_classdefs(module_file: MypyFile) -> Iterator[ClassDef]:
    for defn in module_file.defs:
        if isinstance(defn, ClassDef):
            yield defn


def get_related_field_type(rvalue: CallExpr, api: SemanticAnalyzerPass2,
                           related_model_typ: TypeInfo) -> Optional[Instance]:
    if rvalue.callee.name in {'ForeignKey', 'ManyToManyField'}:
        return api.named_type_or_none(helpers.RELATED_MANAGER_CLASS_FULLNAME,
                                      args=[Instance(related_model_typ, [])])
    else:
        return Instance(related_model_typ, [])


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


def process_model_class(ctx: ClassDefContext) -> None:
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

    # allow unspecified attributes for now
    ctx.cls.info.fallback_to_any = True
