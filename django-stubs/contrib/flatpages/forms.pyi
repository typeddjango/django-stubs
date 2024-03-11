from typing import Any, Literal, Sequence, TypeVar

from django import forms
from django.contrib.flatpages.models import FlatPage

_FlatPage = TypeVar("_FlatPage", bound=FlatPage)

class FlatpageForm(forms.ModelForm[_FlatPage]):
    class Meta:
        model: type[_FlatPage] = ...
        fields: Sequence[str] | Literal['__all__'] = ...

    url: Any
    def clean_url(self) -> str: ...
