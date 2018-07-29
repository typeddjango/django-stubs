from django.template.base import (
    Parser,
    Token,
)
from django.templatetags.static import StaticNode


def do_static(
    parser: Parser,
    token: Token
) -> StaticNode: ...