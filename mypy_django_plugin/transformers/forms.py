from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import AssignmentStmt, NameExpr, RefExpr, TypeInfo
from mypy.types import AnyType, TypeOfAny, get_proper_type

from mypy_django_plugin.lib import fullnames, helpers

if TYPE_CHECKING:
    from mypy.plugin import ClassDefContext
    from mypy.types import Instance


def transform_form_class(ctx: ClassDefContext) -> None:
    make_meta_nested_class_inherit_from_any(ctx)
    bind_model_type_from_meta(ctx)


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
    else:
        meta_node.fallback_to_any = True


def bind_model_type_from_meta(ctx: ClassDefContext) -> None:
    """
    Fill in the model type of a `ModelForm` subclass that omits it, from its `Meta.model`.

    Eg.

        class ArticleForm(forms.ModelForm):
            class Meta:
                model = Article

    is interpreted as:

        class ArticleForm(forms.ModelForm[Article]): ...

    Explicit type args, including `ModelForm[Any]`, are left as written.
    """
    info = ctx.cls.info
    for index, base in enumerate(info.bases):
        if _omits_model_type(base):
            model_info = _get_meta_model(info)
            if model_info is not None:
                info.bases[index] = base.copy_modified(args=[helpers.model_instance(model_info)])
            return


def _omits_model_type(base: Instance) -> bool:
    """Whether `base` is `ModelForm` written without its type arg, which mypy fills with `Any`."""
    if base.type.fullname != fullnames.MODEL_FORM_CLASS_FULLNAME or len(base.args) != 1:
        return False
    model_arg = get_proper_type(base.args[0])
    return isinstance(model_arg, AnyType) and model_arg.type_of_any == TypeOfAny.from_omitted_generics


def _get_meta_model(form_info: TypeInfo) -> TypeInfo | None:
    """The model class assigned to `model` in the form's own `class Meta`."""
    meta_info = helpers.get_nested_meta_node_for_current_class(form_info)
    if meta_info is None:
        return None
    for stmt in meta_info.defn.defs.body:
        if (
            # model = <model class>
            isinstance(stmt, AssignmentStmt)
            and len(stmt.lvalues) == 1
            and isinstance(stmt.lvalues[0], NameExpr)
            and stmt.lvalues[0].name == "model"
            and isinstance(stmt.rvalue, RefExpr)
            and isinstance(stmt.rvalue.node, TypeInfo)
            and helpers.is_model_type(stmt.rvalue.node)
        ):
            return stmt.rvalue.node
    return None
