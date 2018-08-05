from datetime import date
from typing import Any, List, Optional, Union

from django.template import Node
from django.template.base import NodeList, Parser, Token
from django.template.context import Context
from django.utils.safestring import SafeText

register: Any

def localize(value: Union[date, float]) -> str: ...
def unlocalize(value: Union[float, date]) -> str: ...

class LocalizeNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    nodelist: Union[django.template.base.NodeList, List[Any]] = ...
    use_l10n: bool = ...
    def __init__(
        self, nodelist: Union[NodeList, List[Any]], use_l10n: bool
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...

def localize_tag(parser: Parser, token: Token) -> LocalizeNode: ...
