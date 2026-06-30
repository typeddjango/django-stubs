from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.db.utils import ConnectionHandler


def test_in_operator(connections: ConnectionHandler, alias: str) -> None:
    assert_type(alias in connections, bool)
