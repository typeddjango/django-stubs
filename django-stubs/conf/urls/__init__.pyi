from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from typing import (
    Any,
    Optional,
    Union,
)


def url(
    regex: str,
    view: Any,
    kwargs: Any = ...,
    name: Optional[str] = ...
) -> Union[URLPattern, URLResolver]: ...