from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.contrib.flatpages.sitemaps import FlatPageSitemap
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
        Union[
            Callable,
            Tuple[List[Union[URLPattern, URLResolver]], str, str],
            Tuple[Union[List[URLPattern], List[URLResolver]], None, None],
        ]
    ],
    kwargs: Optional[
        Union[
            Dict[str, Dict[str, Type[FlatPageSitemap]]],
            Dict[str, Dict[str, Sitemap]],
            Dict[str, OrderedDict],
            Dict[str, str],
        ]
    ] = ...,
    name: Optional[str] = ...,
) -> Union[URLPattern, URLResolver]: ...
