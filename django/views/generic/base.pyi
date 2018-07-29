from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    HttpResponseRedirectBase,
)
from django.template.response import TemplateResponse
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Union,
)


class ContextMixin:
    def get_context_data(self, **kwargs) -> Dict[str, object]: ...


class RedirectView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirectBase: ...
    def get_redirect_url(self, *args, **kwargs) -> str: ...
    def options(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect: ...
    def post(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect: ...


class TemplateResponseMixin:
    def get_template_names(self) -> List[str]: ...
    def render_to_response(
        self,
        context: Dict[str, Any],
        **response_kwargs
    ) -> TemplateResponse: ...


class TemplateView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class View:
    def __init__(self, **kwargs) -> None: ...
    def _allowed_methods(self) -> List[str]: ...
    @classmethod
    def as_view(cls, **initkwargs) -> Callable: ...
    def dispatch(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> Union[View, HttpResponse]: ...
    def http_method_not_allowed(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseNotAllowed: ...