from django.forms import Form
from django.forms.formsets import BaseFormSet
from typing_extensions import assert_type


def test_in_operator(formset: BaseFormSet[Form], form: Form | None) -> None:
    assert_type(form in formset, bool)
