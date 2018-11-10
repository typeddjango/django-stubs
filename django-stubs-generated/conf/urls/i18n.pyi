from typing import Any, List, Optional, Tuple, Union

from django.urls.resolvers import URLPattern, URLResolver


def i18n_patterns(
    *urls: Any, prefix_default_language: bool = ...
) -> Union[List[List[Any]], List[URLPattern], List[URLResolver]]: ...
def is_language_prefix_patterns_used(urlconf: str) -> Tuple[bool, bool]: ...

urlpatterns: Any
