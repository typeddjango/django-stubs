from django.forms import Form
from typing_extensions import assert_type


def test_in_operator(form: Form, field: str | int) -> None:
    assert_type(field in form, bool)
