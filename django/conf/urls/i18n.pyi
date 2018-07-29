from django.urls.resolvers import URLResolver
from typing import (
    Any,
    List,
    Tuple,
    Union,
)


def i18n_patterns(
    *urls,
    prefix_default_language = ...
) -> Union[List[List[Any]], List[URLResolver]]: ...


def is_language_prefix_patterns_used(urlconf: str) -> Tuple[bool, bool]: ...