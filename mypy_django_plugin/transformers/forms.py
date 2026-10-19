from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import (
    ARG_POS,
    Argument,
    AssignmentStmt,
    Decorator,
    ListExpr,
    NameExpr,
    StrExpr,
    TempNode,
    TupleExpr,
    TypeInfo,
    Var,
)
from mypy.plugins.common import MethodSpec, add_overloaded_method_to_class
from mypy.types import CallableType, Instance, LiteralType, Overloaded, TypeType, get_proper_type
from mypy.typevars import fill_typevars_with_any

from mypy_django_plugin.lib import fullnames, helpers

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mypy.checker import TypeChecker
    from mypy.plugin import AttributeContext, ClassDefContext
    from mypy.types import Type as MypyType

    from mypy_django_plugin.django.context import DjangoContext


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
    else:
        meta_node.fallback_to_any = True


def _iter_declared_field_names(info: TypeInfo) -> Iterator[str]:
    """
    Yield each class body assigned attribute name, starting from the most-derived class.
    """
    seen: set[str] = set()
    for base_info in info.mro:
        if not base_info.has_base(fullnames.BASEFORM_CLASS_FULLNAME):
            continue
        for stmt in base_info.defn.defs.body:
            if (
                isinstance(stmt, AssignmentStmt)
                and len(stmt.lvalues) == 1
                and isinstance(stmt.lvalues[0], NameExpr)
                # Skip annotation-only declarations (e.g. 'age: forms.IntegerField')
                # These have no value assigned, so they never become actual form fields.
                and not isinstance(stmt.rvalue, TempNode)
            ):
                name = stmt.lvalues[0].name
                if name not in seen:
                    seen.add(name)
                    yield name


def _get_model_form_meta(info: TypeInfo) -> TypeInfo | None:
    """
    Find the 'Meta' class declaring 'model' for a 'ModelForm' whose fields can also be declared implicitly
    via 'Meta.fields'/'Meta.exclude'.
    """
    for base_info in info.mro:
        if not base_info.has_base(fullnames.BASEFORM_CLASS_FULLNAME):
            continue
        meta_sym = base_info.names.get("Meta")
        if meta_sym is not None and isinstance(meta_sym.node, TypeInfo) and "model" in meta_sym.node.names:
            return meta_sym.node
    return None


def _resolve_meta_model_type_info(meta_info: TypeInfo) -> TypeInfo | None:
    model_sym = meta_info.names.get("model")
    if model_sym is None or not isinstance(model_sym.node, Var) or model_sym.node.type is None:
        return None
    model_type = get_proper_type(model_sym.node.type)
    if isinstance(model_type, TypeType) and isinstance(model_type.item, Instance):
        return model_type.item.type
    if isinstance(model_type, CallableType) and model_type.is_type_obj():
        return model_type.type_object()
    return None


def _extract_meta_literal(meta_info: TypeInfo, attr: str) -> str | list[str] | None:
    """
    Statically read 'fields' or 'exclude' literal off a 'ModelForm's 'Meta' class body.
    """
    for stmt in meta_info.defn.defs.body:
        if not (isinstance(stmt, AssignmentStmt) and len(stmt.lvalues) == 1 and isinstance(stmt.lvalues[0], NameExpr)):
            continue
        if stmt.lvalues[0].name != attr:
            continue
        rvalue = stmt.rvalue
        # __all__ field case
        if isinstance(rvalue, StrExpr):
            return rvalue.value
        # Multiple fields case
        if isinstance(rvalue, (ListExpr, TupleExpr)):
            names: list[str] = []
            for item in rvalue.items:
                if not isinstance(item, StrExpr):
                    return None
                names.append(item.value)
            return names
        return None
    return None


def _build_model_form_field_types(
    api: TypeChecker, meta_info: TypeInfo, django_context: DjangoContext
) -> dict[str, MypyType] | None:
    """
    Resolve a 'ModelForm's implicit fields using Django's 'fields_for_model()'. Returns 'None' when the fields can't
    be determined.
    """
    model_info = _resolve_meta_model_type_info(meta_info)
    if model_info is None:
        return None

    model_cls = django_context.get_model_class_by_fullname(model_info.fullname)
    if model_cls is None:
        return None

    fields_value = _extract_meta_literal(meta_info, "fields")
    exclude_value = _extract_meta_literal(meta_info, "exclude")
    if fields_value is None and exclude_value is None:
        # Invalid Django config. 'Meta' needs at least one of 'fields'/'exclude'.
        return None

    if fields_value in (None, "__all__"):
        fields_arg = None
    else:
        fields_arg = fields_value

    if isinstance(exclude_value, list):
        exclude_arg = exclude_value
    else:
        exclude_arg = None

    from django.forms.models import fields_for_model

    try:
        runtime_fields = fields_for_model(model_cls, fields=fields_arg, exclude=exclude_arg)
    except Exception:
        return None

    field_types: dict[str, MypyType] = {}
    for name, field_obj in runtime_fields.items():
        if field_obj is None:
            continue
        field_info = helpers.lookup_class_typeinfo(api, type(field_obj))
        if field_info is None:
            continue
        field_types[name] = fill_typevars_with_any(field_info)
    return field_types


def _collect_form_field_types(api: TypeChecker, info: TypeInfo, django_context: DjangoContext) -> dict[str, MypyType]:
    field_types: dict[str, MypyType] = {}

    # Taking types from ModelForm Meta class
    meta_info = _get_model_form_meta(info)
    if meta_info is not None:
        implicit = _build_model_form_field_types(api, meta_info, django_context)
        if implicit is not None:
            field_types.update(implicit)

    # Taking types from statically-declared fields in the form class body
    for name in _iter_declared_field_names(info):
        symbol = info.get(name)
        if symbol is None or not isinstance(symbol.node, Var) or symbol.node.type is None:
            continue
        var_type = get_proper_type(symbol.node.type)
        if isinstance(var_type, Instance) and var_type.type.has_base(fullnames.FORM_FIELD_CLASS_FULLNAME):
            field_types[name] = symbol.node.type

    return field_types


def _get_or_build_fields_dict_type(
    ctx: AttributeContext, info: TypeInfo, django_context: DjangoContext
) -> TypeInfo | None:
    """
    Build a form fields type to extend 'Form.fields'. Every statically-declared field gets typed by
    overloading '__getitem__'.
    """
    api = helpers.get_typechecker_api(ctx)

    metadata = helpers.get_django_metadata(info)
    cached_fullname = metadata.get("form_fields_dict_type", None)
    if cached_fullname is not None:
        if not cached_fullname:
            return None
        return helpers.lookup_fully_qualified_typeinfo(api, cached_fullname)

    field_types = _collect_form_field_types(api, info, django_context)
    if not field_types:
        metadata["form_fields_dict_type"] = ""
        return None

    dict_info = helpers.lookup_fully_qualified_typeinfo(api, "builtins.dict")
    field_base_info = helpers.lookup_fully_qualified_typeinfo(api, fullnames.FORM_FIELD_CLASS_FULLNAME)
    if dict_info is None or field_base_info is None:
        metadata["form_fields_dict_type"] = ""
        return None

    str_instance = api.named_type("builtins.str")
    field_base_instance = fill_typevars_with_any(field_base_info)

    module = api.modules[info.module_name]
    fields_dict_info = helpers.add_new_class_for_module(
        module,
        name=info.name + "_FieldsDict",
        bases=[Instance(dict_info, [str_instance, field_base_instance])],
    )

    # One overload per known field name, then a plain 'str -> Field' as fallback, so unknown/dynamic keys still
    # resolve instead of erroring.
    method_specs = [
        MethodSpec(
            args=[Argument(Var("key"), LiteralType(name, fallback=str_instance), None, ARG_POS)],
            return_type=field_type,
        )
        for name, field_type in field_types.items()
    ]
    method_specs.append(
        MethodSpec(
            args=[Argument(Var("key"), str_instance, None, ARG_POS)],
            return_type=field_base_instance,
        )
    )
    overload_def = add_overloaded_method_to_class(api, fields_dict_info.defn, "__getitem__", method_specs)
    call_types = [
        item.func.type
        for item in overload_def.items
        if isinstance(item, Decorator) and isinstance(item.func.type, CallableType)
    ]
    overload_def.type = Overloaded(call_types)

    metadata["form_fields_dict_type"] = fields_dict_info.fullname
    return fields_dict_info


def transform_form_fields_attr_type(ctx: AttributeContext, *, django_context: DjangoContext) -> MypyType:
    """
    Type 'form.fields' with the synthetic dict built by '_get_or_build_fields_dict_type', using 'dict[str, Field]'
    as fallback.
    """
    if ctx.is_lvalue:
        return ctx.default_attr_type

    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_attr_type

    fields_dict_info = _get_or_build_fields_dict_type(ctx, object_type.type, django_context)
    if fields_dict_info is None:
        return ctx.default_attr_type

    return Instance(fields_dict_info, [])
