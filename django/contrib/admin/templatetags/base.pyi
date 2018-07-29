from django.template.base import (
    Parser,
    Token,
)
from django.template.context import Context
from django.utils.safestring import SafeText
from typing import Callable


class InclusionAdminNode:
    def __init__(
        self,
        parser: Parser,
        token: Token,
        func: Callable,
        template_name: str,
        takes_context: bool = ...
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...