from django.forms import Form
from typing_extensions import assert_type


def test_in_operator(form: Form, field: str) -> None:
    # Valid: str field name
    assert_type(field in form, bool)

    # Invalid: non-str types should error
    _ = 123 in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]
    _ = None in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]
    _ = b"field" in form  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue]  # pyrefly: ignore[unsupported-operation]  # ty: ignore[unsupported-operator]
