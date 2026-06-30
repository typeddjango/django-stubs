from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from typing_extensions import assert_type


def test_in_operator(ctx: CaptureQueriesContext, query: dict[str, str]) -> None:
    assert_type(query in ctx, bool)


def test_iteration(ctx: CaptureQueriesContext) -> None:
    for query in ctx:
        assert_type(query, dict[str, str])


@override_settings(FOO="bar")
def test() -> None:
    pass


assert_type(test(), None)
