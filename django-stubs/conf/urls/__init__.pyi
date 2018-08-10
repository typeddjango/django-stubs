from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from django.contrib.sitemaps import Sitemap
from django.urls import include as include
from django.urls.resolvers import URLPattern, URLResolver

handler400: Any
handler403: Any
handler404: Any
handler500: Any

def url(
    regex: str,
    view: Optional[
        Union[Callable, Tuple[None, None, None], Tuple[str, str, str]]
    ],
    kwargs: Optional[
        Union[
            Dict[str, Dict[str, Sitemap]],
            Dict[str, Union[Dict[str, Type[Sitemap]], str]],
            Dict[str, Union[int, str]],
        ]
    ] = ...,
    name: Optional[str] = ...,
) -> Union[URLPattern, URLResolver]: ...
