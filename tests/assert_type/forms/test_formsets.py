from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.forms import Form
    from django.forms.formsets import BaseFormSet


def test_in_operator(formset: BaseFormSet[Form], form: Form) -> None:
    assert_type(form in formset, bool)
