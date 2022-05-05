from typing import List, Tuple

from django.urls import _AnyURL

def i18n_patterns(*urls: _AnyURL, prefix_default_language: bool = ...) -> List[_AnyURL]: ...
def is_language_prefix_patterns_used(urlconf: str) -> Tuple[bool, bool]: ...

urlpatterns: List[_AnyURL]
