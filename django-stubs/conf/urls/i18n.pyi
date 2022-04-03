from typing import Callable, List, Tuple, Union

from django.urls.resolvers import URLPattern, URLResolver

def i18n_patterns(
    *urls: Union[URLPattern, URLResolver], prefix_default_language: bool = ...
) -> List[Union[URLPattern, URLResolver]]: ...
def is_language_prefix_patterns_used(urlconf: str) -> Tuple[bool, bool]: ...

urlpatterns: List[Callable]
