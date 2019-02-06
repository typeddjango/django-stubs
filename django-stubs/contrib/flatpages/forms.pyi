from typing import Any, Dict, Optional, Union

from django import forms
from django.db.models.query import QuerySet

class FlatpageForm(forms.ModelForm):
    auto_id: str
    data: Dict[str, Union[List[int], str]]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[str, Union[List[django.contrib.sites.models.Site], int, str]]
    instance: django.contrib.flatpages.models.FlatPage
    is_bound: bool
    label_suffix: str
    url: Any = ...
    def clean_url(self) -> str: ...
    def clean(self) -> Dict[str, Union[bool, QuerySet, str]]: ...
