from typing import Any, Optional, Tuple, Union

from .resolvers import (LocalePrefixPattern, RegexPattern, RoutePattern,
                        URLPattern, URLResolver)


def include(
    arg: Any, namespace: Optional[str] = ...
) -> Union[Tuple[str, str, str], Tuple[None, None, None]]: ...

path: Any
re_path: Any
