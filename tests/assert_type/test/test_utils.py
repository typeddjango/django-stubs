from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from typing_extensions import assert_type


def test_in_operator(ctx: CaptureQueriesContext, query: dict[str, str]) -> None:
    assert_type(query in ctx, bool)


@override_settings(FOO="bar")
def test() -> None:
    pass


assert_type(test(), None)
