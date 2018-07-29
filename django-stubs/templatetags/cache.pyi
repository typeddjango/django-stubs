from django.template.base import (
    FilterExpression,
    NodeList,
    Parser,
    Token,
)
from django.template.context import Context
from django.utils.safestring import SafeText
from typing import List


def do_cache(
    parser: Parser,
    token: Token
) -> CacheNode: ...


class CacheNode:
    def __init__(
        self,
        nodelist: NodeList,
        expire_time_var: FilterExpression,
        fragment_name: str,
        vary_on: List[FilterExpression],
        cache_name: None
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...