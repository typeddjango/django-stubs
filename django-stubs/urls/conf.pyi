from typing import Any, Callable, List, Optional, Tuple, Union

from django.urls.resolvers import URLPattern, URLResolver

from .resolvers import (LocalePrefixPattern, RegexPattern, RoutePattern,
                        URLPattern, URLResolver)


def include(
    arg: Union[
        List[Tuple[str, Callable]],
        List[URLPattern],
        List[URLResolver],
        Tuple[List[URLPattern], str, str],
        Tuple[str, str],
        str,
    ],
    namespace: Optional[str] = ...,
) -> Union[Tuple[None, None, None], Tuple[str, str, str]]: ...

path: Any
re_path: Any
