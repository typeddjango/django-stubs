from typing import Any, Callable, Dict, List, Tuple

from django.utils.safestring import SafeString

docutils_is_available: bool

def get_view_name(view_func: Callable) -> str: ...
def parse_docstring(docstring: str) -> Tuple[str, str, Dict[str, str]]: ...
def parse_rst(text: str, default_reference_context: Any, thing_being_parsed: Any | None = ...) -> SafeString: ...

ROLES: Dict[str, str]

def create_reference_role(rolename: str, urlbase: str) -> None: ...
def default_reference_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: Any,
    inliner: Any,
    options: Any | None = ...,
    content: Any | None = ...,
) -> Tuple[List[Any], List[Any]]: ...

named_group_matcher: Any
unnamed_group_matcher: Any

def replace_named_groups(pattern: str) -> str: ...
def replace_unnamed_groups(pattern: str) -> str: ...
