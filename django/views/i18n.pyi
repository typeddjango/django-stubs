from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


def get_formats() -> Dict[str, Union[str, int, List[str]]]: ...


def set_language(request: WSGIRequest) -> HttpResponseRedirect: ...


class JSONCatalog:
    def render_to_response(
        self,
        context: Dict[str, Union[Dict[str, Union[str, List[str]]], Dict[str, Union[str, int, List[str]]], str]],
        **response_kwargs
    ) -> JsonResponse: ...


class JavaScriptCatalog:
    @property
    def _num_plurals(self) -> int: ...
    @property
    def _plural_string(self) -> Optional[str]: ...
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse: ...
    def get_catalog(self) -> Dict[str, Union[str, List[str]]]: ...
    def get_context_data(self, **kwargs) -> Dict[str, Any]: ...
    def get_paths(self, packages: List[str]) -> List[str]: ...
    def get_plural(self) -> Optional[str]: ...
    def render_to_response(
        self,
        context: Dict[str, Optional[Union[Dict[str, str], Dict[str, Union[str, int, List[str]]], Dict[str, Union[str, List[str]]]]]],
        **response_kwargs
    ) -> HttpResponse: ...