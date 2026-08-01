from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import Lookup
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.fields.json import CaseInsensitiveMixin
    from django.db.models.sql.compiler import SQLCompiler


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


def test_case_insensitive_mixin(
    mixin: CaseInsensitiveMixin, compiler: SQLCompiler, connection: BaseDatabaseWrapper
) -> None:
    assert_type(mixin.process_lhs(compiler, connection), tuple[str, tuple[str | int, ...]])
