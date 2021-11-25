from typing import Any, Callable, List, Tuple

from django.urls.resolvers import URLPattern

def i18n_patterns(*urls: Any, prefix_default_language: bool = ...) -> List[List[URLPattern]]: ...
def is_language_prefix_patterns_used(urlconf: str) -> Tuple[bool, bool]: ...

urlpatterns: List[Callable]
