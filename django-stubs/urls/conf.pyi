from typing import Any, Callable, List, Optional, Tuple, Union

from .resolvers import URLPattern, URLResolver

def include(
    arg: Union[List[Tuple[str, Callable]], List[URLPattern], List[URLResolver], Tuple[List[URLResolver], str], str],
    namespace: Optional[str] = ...,
) -> Union[Tuple[List[Any], str, str], Tuple[List[URLResolver], None, None]]: ...

path: Any
re_path: Any
