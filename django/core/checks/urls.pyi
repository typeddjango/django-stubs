from django.core.checks.messages import (
    Error,
    Warning,
)
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from typing import (
    Any,
    Callable,
    List,
    Tuple,
    Union,
)


def E006(name: str) -> Error: ...


def _load_all_namespaces(resolver: URLResolver, parents: Tuple = ...) -> List[str]: ...


def check_resolver(
    resolver: Union[URLPattern, URLResolver]
) -> Union[List[Warning], List[Error]]: ...


def check_url_config(app_configs: None, **kwargs) -> List[Warning]: ...


def check_url_namespaces_unique(app_configs: None, **kwargs) -> List[Any]: ...


def check_url_settings(app_configs: None, **kwargs) -> List[Error]: ...


def get_warning_for_invalid_pattern(pattern: Tuple[str, Callable]) -> List[Error]: ...