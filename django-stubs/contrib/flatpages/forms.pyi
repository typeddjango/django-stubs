from typing import Any

from django import forms
from django.contrib.flatpages.models import FlatPage

class FlatpageForm(forms.ModelForm[FlatPage]):
    url: Any
    def clean_url(self) -> str: ...
