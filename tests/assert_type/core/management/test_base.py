from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from django.core.management.base import CommandParser


def parser_error_never_returns(parser: CommandParser) -> NoReturn:
    parser.error("boom")
