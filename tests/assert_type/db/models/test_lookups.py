from typing import Any

from django.db.models import Lookup
from typing_extensions import assert_type


# Lookup can be used without explicit type argument (defaults to Any).
# Regression test for https://github.com/typeddjango/django-stubs/issues/2649.
def test_lookup_optional_type_arg(lookup: Lookup, typed_lookup: Lookup[int]) -> None:
    assert_type(lookup, Lookup)
    assert_type(typed_lookup, Lookup[int])


class MyLookup(Lookup): ...


class MyTypedLookup(Lookup[Any]): ...


def test_subclass_without_type_arg(lookup: MyLookup, typed: MyTypedLookup) -> None:
    # MyLookup(Lookup) is equivalent to MyLookup(Lookup[Any])
    assert_type(lookup, MyLookup)
    assert_type(typed, MyTypedLookup)
