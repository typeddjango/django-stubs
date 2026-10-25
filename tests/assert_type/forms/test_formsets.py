from __future__ import annotations

from typing import assert_type

from django.forms import Form
from django.forms.formsets import BaseFormSet, formset_factory


def test_in_operator(formset: BaseFormSet[Form], form: Form) -> None:
    assert_type(form in formset, bool)


class ContactForm(Form): ...


ContactFormSet = formset_factory(ContactForm)
assert_type(ContactFormSet, type[BaseFormSet[ContactForm]])
assert_type(ContactFormSet().forms, list[ContactForm])
