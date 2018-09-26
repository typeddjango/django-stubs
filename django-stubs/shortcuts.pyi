from typing import Any, Callable, Dict, List, Optional, Type, Union

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect


def render_to_response(
    template_name: Union[List[str], str],
    context: Optional[Dict[str, str]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def render(
    request: WSGIRequest,
    template_name: Union[List[str], str],
    context: Optional[Dict[str, bool]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def redirect(
    to: Union[Callable, str], *args: Any, permanent: bool = ..., **kwargs: Any
) -> HttpResponseRedirect: ...
def get_object_or_404(
    klass: Union[Type[Model], Manager, QuerySet, str], *args: Any, **kwargs: Any
) -> Model: ...
def get_list_or_404(
    klass: Union[List[Type[Model]], Manager, QuerySet],
    *args: Any,
    **kwargs: Any
) -> List[Model]: ...
def resolve_url(
    to: Union[Callable, Model, str], *args: Any, **kwargs: Any
) -> str: ...
