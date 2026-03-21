from django.db.utils import ConnectionHandler
from typing_extensions import assert_type


def test_in_operator(connections: ConnectionHandler, alias: str | int) -> None:
    assert_type(alias in connections, bool)
