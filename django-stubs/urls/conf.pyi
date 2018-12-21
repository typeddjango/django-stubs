from typing import Any, Callable, List, Optional, Tuple, Union

from .resolvers import URLPattern, URLResolver

def include(
    arg: Union[List[Tuple[str, Callable]], List[URLPattern], List[URLResolver], Tuple[List[URLResolver], str], str],
    namespace: Optional[str] = ...,
) -> Tuple[List[URLResolver], Optional[str], Optional[str]]: ...

path: Any
re_path: Any
