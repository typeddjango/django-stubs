from collections import UserList
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.forms.renderers import BaseRenderer
from django.utils.datastructures import MultiValueDict
from django.utils.functional import _StrOrPromise
from django.utils.safestring import SafeString
from typing_extensions import TypeAlias

_DataT: TypeAlias = Mapping[str, Any]  # noqa: PYI047

_FilesT: TypeAlias = MultiValueDict[str, UploadedFile]  # noqa: PYI047

def pretty_name(name: str) -> str: ...
def flatatt(attrs: dict[str, Any]) -> SafeString: ...

class RenderableMixin:
    def get_context(self) -> dict[str, Any]: ...
    def render(
        self,
        template_name: str | None = ...,
        context: dict[str, Any] | None = ...,
        renderer: BaseRenderer | type[BaseRenderer] | None = ...,
    ) -> SafeString: ...
    __str__ = render
    __html__ = render

class RenderableFormMixin(RenderableMixin):
    def as_p(self) -> SafeString: ...
    def as_table(self) -> SafeString: ...
    def as_ul(self) -> SafeString: ...
    def as_div(self) -> SafeString: ...

class RenderableErrorMixin(RenderableMixin):
    def as_json(self, escape_html: bool = ...) -> str: ...
    def as_text(self) -> SafeString: ...
    def as_ul(self) -> SafeString: ...

class ErrorDict(dict[str, ErrorList], RenderableErrorMixin):
    template_name: str
    template_name_text: str
    template_name_ul: str
    renderer: BaseRenderer

    def __init__(self, *args: Any, renderer: BaseRenderer | None = None, **kwargs: Any): ...
    def as_data(self) -> dict[str, list[ValidationError]]: ...
    def get_json_data(self, escape_html: bool = ...) -> dict[str, Any]: ...

class ErrorList(UserList[ValidationError | _StrOrPromise], RenderableErrorMixin):
    template_name: str
    template_name_text: str
    template_name_ul: str
    error_class: str
    renderer: BaseRenderer
    def __init__(
        self,
        initlist: ErrorList | Sequence[str | Exception] | None = ...,
        error_class: str | None = ...,
        renderer: BaseRenderer | None = ...,
    ) -> None: ...
    def as_data(self) -> list[ValidationError]: ...
    def get_json_data(self, escape_html: bool = ...) -> list[dict[str, str]]: ...

def from_current_timezone(value: datetime) -> datetime: ...
def to_current_timezone(value: datetime) -> datetime: ...
