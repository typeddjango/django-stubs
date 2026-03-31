from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import override_settings
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.test.utils import CaptureQueriesContext


def test_in_operator(ctx: CaptureQueriesContext, query: dict[str, str]) -> None:
    assert_type(query in ctx, bool)


@override_settings(FOO="bar")
def test() -> None:
    pass


assert_type(test(), None)
