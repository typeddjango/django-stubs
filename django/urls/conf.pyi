from django.urls.resolvers import (
    CheckURLMixin,
    URLPattern,
    URLResolver,
)
from typing import (
    Any,
    Optional,
    Type,
    Union,
)


def _path(
    route: str,
    view: Any,
    kwargs: Any = ...,
    name: Optional[str] = ...,
    Pattern: Type[CheckURLMixin] = ...
) -> Union[URLPattern, URLResolver]: ...


def include(arg: Any, namespace: Optional[str] = ...) -> Any: ...