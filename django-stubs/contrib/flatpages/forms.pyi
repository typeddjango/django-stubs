from typing import Any

from django import forms
from django.db.models import Model

class FlatpageForm(forms.ModelForm[Model]):
    url: Any
    def clean_url(self) -> str: ...
