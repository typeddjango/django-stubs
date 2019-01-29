from typing import Any, Callable, Dict, List, Optional, Type, Union

from django.db.models.base import Model, Manager, QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect

from django.http import HttpRequest

def render_to_response(
    template_name: str,
    context: Optional[Dict[str, Any]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def render(
    request: HttpRequest,
    template_name: str,
    context: Optional[Dict[str, Any]] = ...,
    content_type: Optional[str] = ...,
    status: Optional[int] = ...,
    using: Optional[str] = ...,
) -> HttpResponse: ...
def redirect(to: Union[Callable, str], *args: Any, permanent: bool = ..., **kwargs: Any) -> HttpResponseRedirect: ...
def get_object_or_404(klass: Union[Type[Model], Type[Manager], QuerySet], *args: Any, **kwargs: Any) -> Model: ...
def get_list_or_404(klass: List[Type[Model]], *args: Any, **kwargs: Any) -> List[Model]: ...
def resolve_url(to: Union[Callable, Model, str], *args: Any, **kwargs: Any) -> str: ...
