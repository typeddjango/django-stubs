from django.urls.resolvers import ResolverMatch
from typing import (
    Any,
    Callable,
    Optional,
    Type,
    Union,
)


def clear_url_caches() -> None: ...


def get_script_prefix() -> str: ...


def get_urlconf(default: None = ...) -> Optional[Union[str, Type[object]]]: ...


def is_valid_path(path: str, urlconf: Optional[str] = ...) -> bool: ...


def resolve(path: str, urlconf: Optional[str] = ...) -> ResolverMatch: ...


def reverse(
    viewname: Optional[Union[str, Callable]],
    urlconf: Optional[str] = ...,
    args: Any = ...,
    kwargs: Any = ...,
    current_app: Optional[str] = ...
) -> str: ...


def set_script_prefix(prefix: str) -> None: ...


def set_urlconf(urlconf_name: Optional[Union[Type[object], str]]) -> None: ...


def translate_url(url: str, lang_code: str) -> str: ...