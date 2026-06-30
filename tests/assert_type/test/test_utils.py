from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import override_settings
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.test.utils import CaptureQueriesContext


def test_in_operator(ctx: CaptureQueriesContext, query: dict[str, str]) -> None:
    assert_type(query in ctx, bool)


def test_iteration(ctx: CaptureQueriesContext) -> None:
    for query in ctx:
        assert_type(query, dict[str, str])


@override_settings(FOO="bar")
def test() -> None:
    pass


assert_type(test(), None)
