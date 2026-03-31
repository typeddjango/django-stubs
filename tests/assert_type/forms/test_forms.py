from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.forms import Form


def test_in_operator(form: Form, field: str) -> None:
    # Valid: str field name
    assert_type(field in form, bool)

    # Invalid: non-str types should error
    _ = 123 in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]
    _ = None in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]
    _ = b"field" in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]


# SuccessMessageMixin is compatible with FormMixin
class FormFirstView(FormMixin[Any], SuccessMessageMixin[Any]):
    pass


class SuccessMessageFirstView(SuccessMessageMixin[Any], FormMixin[Any]):
    pass
