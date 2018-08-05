from typing import Any, Callable, Dict, List, Optional, Type, Union

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.http.response import HttpResponse, HttpResponseRedirect


def render_to_response(
    template_name: Union[str, List[str]],
    context: Optional[Dict[str, str]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def render(
    request: WSGIRequest,
    template_name: Union[str, List[str]],
    context: Optional[
        Union[
            Dict[str, bool],
            Dict[str, Union[Form, str]],
            Dict[str, Union[Manager, QuerySet]],
            Dict[str, Union[str, None]],
        ]
    ] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def redirect(
    to: Union[str, Callable], *args: Any, permanent: bool = ..., **kwargs: Any
) -> HttpResponseRedirect: ...
def get_object_or_404(
    klass: Union[QuerySet, Type[Model], str, Manager], *args: Any, **kwargs: Any
) -> Model: ...
def get_list_or_404(
    klass: Union[QuerySet, List[Type[Model]], Manager],
    *args: Any,
    **kwargs: Any
) -> List[Model]: ...
def resolve_url(
    to: Union[str, Model, Callable], *args: Any, **kwargs: Any
) -> str: ...
