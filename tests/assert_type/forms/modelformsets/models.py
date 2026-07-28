from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.forms.models import BaseInlineFormSet, BaseModelFormSet, ModelForm
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
    from django.forms.models import ModelChoiceField, ModelChoiceIterator


class Author(models.Model):
    pass


class Book(models.Model):
    pass


def test_form_parameter_defaults_to_model_form() -> None:
    """`_ModelFormT` defaults to `ModelForm[_M]`, so the form parameter can be omitted."""

    class AuthorForm(ModelForm[Author]): ...

    implicit: BaseModelFormSet[Author] = BaseModelFormSet()
    explicit: BaseModelFormSet[Author, AuthorForm] = BaseModelFormSet()
    # `ty` doesn't substitute `_M` in the default yet, it infers `list[ModelForm[Unknown]]`.
    assert_type(implicit.saved_forms, "list[ModelForm[Author]]")  # ty: ignore[type-assertion-failure]
    assert_type(explicit.saved_forms, "list[AuthorForm]")


def test_inline_form_parameter_defaults_to_model_form(
    inline: BaseInlineFormSet[Book, Author],
    generic_inline: BaseGenericInlineFormSet[Book],
) -> None:
    assert_type(inline.saved_forms, "list[ModelForm[Book]]")  # ty: ignore[type-assertion-failure]
    assert_type(inline.save(), "list[Book]")
    assert_type(generic_inline.saved_forms, "list[ModelForm[Book]]")  # ty: ignore[type-assertion-failure]


def test_model_choice_iterator(field: ModelChoiceField[Author], iterator: ModelChoiceIterator[Author]) -> None:
    """`ModelChoiceIterator` is generic over the model of its field."""
    assert_type(field.iterator, "type[ModelChoiceIterator[Author]]")
    assert_type(iterator.field, "ModelChoiceField[Author]")
    assert_type(iterator.queryset, "models.QuerySet[Author]")
