from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from uuid import UUID

from django.contrib.sitemaps import Sitemap
from django.core.checks.messages import CheckMessage, Warning
from django.utils.datastructures import MultiValueDict

from .converters import get_converter
from .exceptions import NoReverseMatch, Resolver404
from .utils import get_callable


class ResolverMatch:
    func: Callable = ...
    args: Tuple = ...
    kwargs: Union[
        Dict[str, Dict[str, django.contrib.sitemaps.Sitemap]],
        Dict[str, Union[Dict[str, Type[django.contrib.sitemaps.Sitemap]], str]],
        Dict[str, Union[int, str]],
        Dict[str, bytes],
        Dict[str, uuid.UUID],
    ] = ...
    url_name: Optional[str] = ...
    app_names: List[str] = ...
    app_name: str = ...
    namespaces: List[str] = ...
    namespace: str = ...
    view_name: str = ...
    def __init__(
        self,
        func: Callable,
        args: Tuple,
        kwargs: Union[
            Dict[str, Dict[str, Sitemap]],
            Dict[str, Union[Dict[str, Type[Sitemap]], str]],
            Dict[str, Union[int, str]],
            Dict[str, bytes],
            Dict[str, UUID],
        ],
        url_name: Optional[str] = ...,
        app_names: Optional[List[Optional[str]]] = ...,
        namespaces: Optional[List[Optional[str]]] = ...,
    ) -> None: ...
    def __getitem__(
        self, index: int
    ) -> Union[
        Callable,
        Dict[str, Dict[str, Sitemap]],
        Dict[str, Union[Dict[str, Type[Sitemap]], str]],
        Dict[str, Union[int, str]],
        Tuple,
    ]: ...

def get_resolver(
    urlconf: Optional[Union[Type[Any], str]] = ...
) -> URLResolver: ...
def get_ns_resolver(
    ns_pattern: str, resolver: URLResolver, converters: Tuple
) -> URLResolver: ...

class LocaleRegexDescriptor:
    attr: str = ...
    def __init__(self, attr: Any) -> None: ...
    def __get__(
        self, instance: Optional[RegexPattern], cls: Type[RegexPattern] = ...
    ) -> LocaleRegexDescriptor: ...

class CheckURLMixin:
    def describe(self) -> str: ...

class RegexPattern(CheckURLMixin):
    regex: Any = ...
    name: Optional[str] = ...
    converters: Dict[Any, Any] = ...
    def __init__(
        self, regex: str, name: Optional[str] = ..., is_endpoint: bool = ...
    ) -> None: ...
    def match(
        self, path: str
    ) -> Optional[Tuple[str, Tuple, Dict[str, str]]]: ...
    def check(self) -> List[Warning]: ...

class RoutePattern(CheckURLMixin):
    regex: Any = ...
    name: Optional[str] = ...
    converters: Union[
        Dict[
            str,
            Union[
                django.urls.converters.IntConverter,
                django.urls.converters.StringConverter,
            ],
        ],
        Dict[str, django.urls.converters.UUIDConverter],
    ] = ...
    def __init__(
        self, route: str, name: Optional[str] = ..., is_endpoint: bool = ...
    ) -> None: ...
    def match(
        self, path: str
    ) -> Optional[
        Tuple[
            str,
            Tuple,
            Union[
                Dict[str, Union[int, str]], Dict[str, bytes], Dict[str, UUID]
            ],
        ]
    ]: ...
    def check(self) -> List[Warning]: ...

class LocalePrefixPattern:
    prefix_default_language: bool = ...
    converters: Dict[Any, Any] = ...
    def __init__(self, prefix_default_language: bool = ...) -> None: ...
    @property
    def regex(self): ...
    @property
    def language_prefix(self) -> str: ...
    def match(
        self, path: str
    ) -> Optional[Tuple[str, Tuple, Dict[Any, Any]]]: ...
    def check(self) -> List[Any]: ...
    def describe(self) -> str: ...

class URLPattern:
    lookup_str: str
    pattern: django.urls.resolvers.CheckURLMixin = ...
    callback: Callable = ...
    default_args: Union[
        Dict[str, Dict[str, django.contrib.sitemaps.Sitemap]],
        Dict[str, Union[Dict[str, Type[django.contrib.sitemaps.Sitemap]], str]],
        Dict[str, Union[int, str]],
    ] = ...
    name: Optional[str] = ...
    def __init__(
        self,
        pattern: CheckURLMixin,
        callback: Callable,
        default_args: Optional[
            Union[
                Dict[str, Dict[str, Sitemap]],
                Dict[str, Union[Dict[str, Type[Sitemap]], str]],
                Dict[str, Union[int, str]],
            ]
        ] = ...,
        name: Optional[str] = ...,
    ) -> None: ...
    def check(self) -> List[Warning]: ...
    def resolve(self, path: str) -> Optional[ResolverMatch]: ...
    def lookup_str(self) -> str: ...

class URLResolver:
    url_patterns: Union[
        List[Tuple[str, Callable]],
        List[
            Union[
                django.urls.resolvers.URLPattern,
                django.urls.resolvers.URLResolver,
            ]
        ],
    ]
    urlconf_module: Optional[
        Union[
            List[Tuple[str, Callable]],
            List[
                Union[
                    django.urls.resolvers.URLPattern,
                    django.urls.resolvers.URLResolver,
                ]
            ],
            Type[Any],
        ]
    ]
    pattern: Union[
        django.urls.resolvers.CheckURLMixin,
        django.urls.resolvers.LocalePrefixPattern,
    ] = ...
    urlconf_name: Optional[
        Union[
            List[List[Any]],
            List[Tuple[str, Callable]],
            List[
                Union[
                    django.urls.resolvers.URLPattern,
                    django.urls.resolvers.URLResolver,
                ]
            ],
            Type[Any],
            str,
        ]
    ] = ...
    callback: None = ...
    default_kwargs: Union[Dict[str, Dict[Any, Any]], Dict[str, str]] = ...
    namespace: Optional[str] = ...
    app_name: Optional[str] = ...
    def __init__(
        self,
        pattern: Union[CheckURLMixin, LocalePrefixPattern],
        urlconf_name: Optional[
            Union[
                List[List[Any]],
                List[Tuple[str, Callable]],
                List[Union[URLPattern, URLResolver]],
                Type[Any],
                str,
            ]
        ],
        default_kwargs: Optional[
            Union[Dict[str, Dict[Any, Any]], Dict[str, str]]
        ] = ...,
        app_name: Optional[str] = ...,
        namespace: Optional[str] = ...,
    ) -> None: ...
    def check(self) -> List[CheckMessage]: ...
    @property
    def reverse_dict(self) -> MultiValueDict: ...
    @property
    def namespace_dict(self) -> Dict[str, Tuple[str, URLResolver]]: ...
    @property
    def app_dict(self) -> Dict[str, List[str]]: ...
    def resolve(self, path: str) -> ResolverMatch: ...
    def urlconf_module(
        self
    ) -> Optional[
        Union[
            List[Tuple[str, Callable]],
            List[Union[URLPattern, URLResolver]],
            Type[Any],
        ]
    ]: ...
    def url_patterns(
        self
    ) -> Union[
        List[Tuple[str, Callable]], List[Union[URLPattern, URLResolver]]
    ]: ...
    def resolve_error_handler(
        self, view_type: int
    ) -> Tuple[Callable, Dict[Any, Any]]: ...
    def reverse(self, lookup_view: str, *args: Any, **kwargs: Any) -> str: ...
