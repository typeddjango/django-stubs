import dataclasses
from abc import abstractmethod, ABCMeta
from typing import cast, Iterator, Tuple, Optional, Dict

from mypy.nodes import ClassDef, AssignmentStmt, CallExpr, MemberExpr, StrExpr, NameExpr, MDEF, TypeInfo, Var, SymbolTableNode, \
    Lvalue, Expression, MypyFile, Context
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Instance

from mypy_django_plugin import helpers


@dataclasses.dataclass
class ModelClassInitializer(metaclass=ABCMeta):
    api: SemanticAnalyzerPass2
    model_classdef: ClassDef

    @classmethod
    def from_ctx(cls, ctx: ClassDefContext):
        return cls(api=cast(SemanticAnalyzerPass2, ctx.api), model_classdef=ctx.cls)

    def get_nested_meta_node(self) -> Optional[TypeInfo]:
        metaclass_sym = self.model_classdef.info.names.get('Meta')
        if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
            return metaclass_sym.node
        return None

    def is_abstract_model(self) -> bool:
        meta_node = self.get_nested_meta_node()
        if meta_node is None:
            return False

        for lvalue, rvalue in iter_over_assignments(meta_node.defn):
            if isinstance(lvalue, NameExpr) and lvalue.name == 'abstract':
                is_abstract = self.api.parse_bool(rvalue)
                if is_abstract:
                    # abstract model do not need 'objects' queryset
                    return True
        return False

    def add_new_node_to_model_class(self, name: str, typ: Instance) -> None:
        var = Var(name=name, type=typ)
        var.info = typ.type
        var._fullname = self.model_classdef.info.fullname() + '.' + name
        var.is_inferred = True
        var.is_initialized_in_class = True
        self.model_classdef.info.names[name] = SymbolTableNode(MDEF, var)

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()


def iter_over_assignments(klass: ClassDef) -> Iterator[Tuple[Lvalue, Expression]]:
    for stmt in klass.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) > 1:
            # not supported yet
            continue
        yield stmt.lvalues[0], stmt.rvalue


def iter_call_assignments(klass: ClassDef) -> Iterator[Tuple[Lvalue, CallExpr]]:
    for lvalue, rvalue in iter_over_assignments(klass):
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
            self.add_new_node_to_model_class(lvalue.name + '_id',
                                             typ=self.api.named_type('__builtins__.int'))


class InjectAnyAsBaseForNestedMeta(ModelClassInitializer):
    def run(self) -> None:
        meta_node = self.get_nested_meta_node()
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddDefaultObjectsManager(ModelClassInitializer):
    def is_default_objects_attr(self, sym: SymbolTableNode) -> bool:
        return sym.fullname == helpers.MODEL_CLASS_FULLNAME + '.' + 'objects'

    def run(self) -> None:
        existing_objects_sym = self.model_classdef.info.get('objects')
        if (existing_objects_sym is not None
            and not self.is_default_objects_attr(existing_objects_sym)):
            return None

        if self.is_abstract_model():
            # abstract models do not need 'objects' queryset
            return None

        typ = self.api.named_type_or_none(helpers.MANAGER_CLASS_FULLNAME,
                                          args=[Instance(self.model_classdef.info, [])])
        if not typ:
            return None
        self.add_new_node_to_model_class('objects', typ)


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
            self.add_new_node_to_model_class('id', self.api.builtin_type('builtins.int'))


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
                        except helpers.InvalidModelString as exc:
                            self.api.fail(f'Invalid value for a to= parameter: {exc.model_string!r}',
                                          Context(line=rvalue.line))
                            return None

                        if self.model_classdef.fullname == ref_to_fullname:
                            if 'related_name' in rvalue.arg_names:
                                related_name_expr = rvalue.args[rvalue.arg_names.index('related_name')]
                                if not isinstance(related_name_expr, StrExpr):
                                    return None
                                related_name = related_name_expr.value
                                typ = get_related_field_type(rvalue, self.api, defn.info)
                                if typ is None:
                                    return None
                                self.add_new_node_to_model_class(related_name, typ)


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
        module = module_file.names[expr.callee.expr.name]
        if module.fullname == 'django.db.models' and expr.callee.name in {'ForeignKey',
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


def process_model_class(ctx: ClassDefContext) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultObjectsManager,
        AddIdAttributeIfPrimaryKeyTrueIsNotSet,
        SetIdAttrsForRelatedFields,
        AddRelatedManagers
    ]
    for initializer_cls in initializers:
        initializer_cls.from_ctx(ctx).run()

    # allow unspecified attributes for now
    ctx.cls.info.fallback_to_any = True
