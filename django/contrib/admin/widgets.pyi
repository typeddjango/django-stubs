from datetime import datetime
from django.contrib.admin.sites import AdminSite
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
    ManyToOneRel,
)
from django.forms.widgets import (
    Media,
    Select,
)
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


def url_params_from_lookup_dict(lookups: Dict[str, Union[str, int]]) -> Dict[str, str]: ...


class AdminDateWidget:
    def __init__(self, attrs: None = ..., format: None = ...) -> None: ...
    @property
    def media(self) -> Media: ...


class AdminEmailInputWidget:
    def __init__(self, attrs: None = ...) -> None: ...


class AdminIntegerFieldWidget:
    def __init__(self, attrs: None = ...) -> None: ...


class AdminSplitDateTime:
    def __init__(self, attrs: None = ...) -> None: ...
    def get_context(
        self,
        name: str,
        value: Optional[datetime],
        attrs: Dict[str, Union[bool, str]]
    ) -> Dict[str, Any]: ...


class AdminTextInputWidget:
    def __init__(self, attrs: None = ...) -> None: ...


class AdminTextareaWidget:
    def __init__(self, attrs: None = ...) -> None: ...


class AdminTimeWidget:
    def __init__(self, attrs: None = ..., format: None = ...) -> None: ...
    @property
    def media(self) -> Media: ...


class AdminURLFieldWidget:
    def __init__(self, attrs: None = ...) -> None: ...
    def get_context(
        self,
        name: str,
        value: None,
        attrs: Dict[str, str]
    ) -> Dict[str, Union[Dict[str, Union[str, bool, None, Dict[str, str]]], str]]: ...


class AutocompleteMixin:
    def __init__(
        self,
        rel: ManyToOneRel,
        admin_site: AdminSite,
        attrs: None = ...,
        choices: Tuple = ...,
        using: None = ...
    ) -> None: ...
    def build_attrs(self, base_attrs: Dict[Any, Any], extra_attrs: Dict[str, str] = ...) -> Dict[str, str]: ...
    def get_url(self) -> str: ...
    @property
    def media(self) -> Media: ...
    def optgroups(
        self,
        name: str,
        value: List[str],
        attr: Dict[str, str] = ...
    ) -> Union[List[Tuple[None, List[Dict[str, Union[str, int, Set[str], Dict[str, bool]]]], int]], List[Tuple[None, List[Dict[str, Union[bool, str]]], int]]]: ...


class FilteredSelectMultiple:
    def __init__(self, verbose_name: str, is_stacked: bool, attrs: None = ..., choices: Tuple = ...) -> None: ...
    @property
    def media(self) -> Media: ...


class ForeignKeyRawIdWidget:
    def __init__(
        self,
        rel: ManyToOneRel,
        admin_site: AdminSite,
        attrs: None = ...,
        using: None = ...
    ) -> None: ...
    def base_url_parameters(self) -> Dict[str, str]: ...
    def get_context(
        self,
        name: str,
        value: None,
        attrs: Dict[str, Union[bool, str]]
    ) -> Dict[str, Union[Dict[str, Union[str, bool, None, Dict[str, Union[bool, str]]]], str]]: ...
    def url_parameters(self) -> Dict[str, str]: ...


class RelatedFieldWidgetWrapper:
    def __deepcopy__(self, memo: Dict[int, Any]) -> RelatedFieldWidgetWrapper: ...
    def __init__(
        self,
        widget: Union[Select, AdminRadioSelect],
        rel: ForeignObjectRel,
        admin_site: AdminSite,
        can_add_related: Optional[bool] = ...,
        can_change_related: bool = ...,
        can_delete_related: bool = ...,
        can_view_related: bool = ...
    ) -> None: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[str, int]],
        attrs: Dict[str, str]
    ) -> Dict[str, Union[bool, str]]: ...
    def get_related_url(self, info: Tuple[str, str], action: str, *args) -> str: ...
    def id_for_label(self, id_: str) -> str: ...
    @property
    def is_hidden(self) -> bool: ...
    @property
    def media(self) -> Media: ...
    def value_from_datadict(
        self,
        data: QueryDict,
        files: MultiValueDict,
        name: str
    ) -> Optional[str]: ...