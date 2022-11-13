from collections.abc import Iterator, Mapping
from typing import Any, Protocol

from django.http.request import HttpRequest
from django.template import TemplateDoesNotExist
from django.template.base import Context
from django.utils.safestring import SafeString

class BaseEngine:
    name: str
    dirs: list[str]
    app_dirs: bool
    def __init__(self, params: Mapping[str, Any]) -> None: ...
    @property
    def app_dirname(self) -> str | None: ...
    def from_string(self, template_code: str) -> _EngineTemplate: ...
    def get_template(self, template_name: str) -> _EngineTemplate: ...
    @property
    def template_dirs(self) -> tuple[str]: ...
    def iter_template_filenames(self, template_name: str) -> Iterator[str]: ...

class _EngineTemplate(Protocol):
    def render(
        self,
        context: Context | dict[str, Any] | None = ...,
        request: HttpRequest | None = ...,
    ) -> SafeString: ...
