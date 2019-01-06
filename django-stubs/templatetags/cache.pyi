from typing import Any, List, Optional

from django.template import Node
from django.template.base import FilterExpression, NodeList, Parser, Token
from django.template.context import Context
from django.utils.safestring import SafeText

register: Any

class CacheNode(Node):
    origin: Origin
    token: Token
    nodelist: NodeList = ...
    expire_time_var: FilterExpression = ...
    fragment_name: str = ...
    vary_on: List[FilterExpression] = ...
    cache_name: Optional[FilterExpression] = ...
    def __init__(
        self,
        nodelist: NodeList,
        expire_time_var: FilterExpression,
        fragment_name: str,
        vary_on: List[FilterExpression],
        cache_name: Optional[FilterExpression],
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...

def do_cache(parser: Parser, token: Token) -> CacheNode: ...
