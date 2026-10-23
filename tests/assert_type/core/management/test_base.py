from __future__ import annotations

from typing import TYPE_CHECKING, Never

if TYPE_CHECKING:
    from django.core.management.base import CommandParser


def parser_error_never_returns(parser: CommandParser) -> Never:
    parser.error("boom")
