from django.test.utils import CaptureQueriesContext
from typing_extensions import assert_type


def test_in_operator(ctx: CaptureQueriesContext, query: dict[str, str] | None) -> None:
    assert_type(query in ctx, bool)
