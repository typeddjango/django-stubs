from typing import Any, Literal, Sequence

from django import forms
from django.contrib.flatpages.models import FlatPage

class FlatpageForm(forms.ModelForm[FlatPage]):
    class Meta:
        model: type[FlatPage] = ...
        fields: Sequence[str] | Literal["__all__"] = ...

    url: Any
    def clean_url(self) -> str: ...
