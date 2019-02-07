from typing import Any, Callable, Dict, List, Optional, Type, Union, Sequence, Protocol

from django.db.models import Manager, QuerySet
from django.db.models.base import Model
from django.http.response import HttpResponse as HttpResponse, HttpResponseRedirect as HttpResponseRedirect

from django.http import HttpRequest

def render_to_response(
    template_name: Union[str, Sequence[str]],
    context: Optional[Dict[str, Any]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def render(
    request: HttpRequest,
    template_name: Union[str, Sequence[str]],
    context: Optional[Dict[str, Any]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...

class SupportsGetAbsoluteUrl(Protocol):
    pass

def redirect(
    to: Union[Callable, str, SupportsGetAbsoluteUrl], *args: Any, permanent: bool = ..., **kwargs: Any
) -> HttpResponseRedirect: ...
def get_object_or_404(klass: Union[Type[Model], Manager, QuerySet], *args: Any, **kwargs: Any) -> Model: ...
def get_list_or_404(klass: Union[Type[Model], Manager, QuerySet], *args: Any, **kwargs: Any) -> List[Model]: ...
def resolve_url(to: Union[Callable, Model, str], *args: Any, **kwargs: Any) -> str: ...
