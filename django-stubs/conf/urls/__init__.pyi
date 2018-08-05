from typing import Any, Callable, Optional, Tuple, Union

from django.urls import include as include
from django.urls.resolvers import URLPattern, URLResolver

handler400: Any
handler403: Any
handler404: Any
handler500: Any

def url(
    regex: str,
    view: Optional[
        Union[Tuple[None, None, None], Tuple[str, str, str], Callable]
    ],
    kwargs: Any = ...,
    name: Optional[str] = ...,
) -> Union[URLResolver, URLPattern]: ...
