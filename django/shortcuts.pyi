from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http.response import (
    HttpResponse,
    HttpResponseRedirect,
)
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
)


def _get_queryset(
    klass: Union[Type[Model], QuerySet, Manager]
) -> Union[QuerySet, Manager]: ...


def get_list_or_404(klass: Manager, *args, **kwargs) -> List[Model]: ...


def get_object_or_404(klass: Type[Model], *args, **kwargs) -> Model: ...


def redirect(
    to: Union[str, Callable],
    *args,
    permanent = ...,
    **kwargs
) -> HttpResponseRedirect: ...


def render(
    request: WSGIRequest,
    template_name: str,
    context: Optional[Union[Dict[str, bool], Dict[str, Union[str, None]], Dict[str, str]]] = ...,
    content_type: None = ...,
    status: Optional[int] = ...,
    using: None = ...
) -> HttpResponse: ...


def render_to_response(
    template_name: str,
    context: Dict[str, str] = ...,
    content_type: str = ...,
    status: None = ...,
    using: None = ...
) -> HttpResponse: ...


def resolve_url(to: Union[str, Callable], *args, **kwargs) -> str: ...