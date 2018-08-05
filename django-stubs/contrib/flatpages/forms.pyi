from typing import Any, Dict, Optional, Union

from django import forms
from django.db.models.query import QuerySet


class FlatpageForm(forms.ModelForm):
    auto_id: str
    data: Dict[str, Union[str, List[int]]]
    empty_permitted: bool
    error_class: Type[django.forms.utils.ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[str, Union[int, str, List[django.contrib.sites.models.Site]]]
    instance: django.contrib.flatpages.models.FlatPage
    is_bound: bool
    label_suffix: str
    url: Any = ...
    class Meta:
        model: Any = ...
        fields: str = ...
    def clean_url(self) -> str: ...
    def clean(self) -> Dict[str, Union[str, bool, QuerySet]]: ...
