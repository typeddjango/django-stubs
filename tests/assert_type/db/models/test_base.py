from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, assert_type

from django.db import models
from typing_extensions import TypeVar, override

if TYPE_CHECKING:
    from collections.abc import Iterable

    from django.db.models.query import QuerySet


class MyModel(models.Model):
    class Meta:
        app_label = "myapp"


class OtherModel(models.Model):
    class Meta:
        app_label = "myapp"


# Override with QuerySet[Model] — valid
class OverrideWithModel(models.Model):
    class Meta:
        app_label = "myapp"

    @override
    def refresh_from_db(
        self,
        using: str | None = None,
        fields: Iterable[str] | None = None,
        from_queryset: QuerySet[models.Model] | None = None,
    ) -> None: ...


def test_correct_queryset(m: MyModel, qs: QuerySet[MyModel]) -> None:
    m.refresh_from_db(from_queryset=qs)
    assert_type(m.refresh_from_db(), None)


def test_wrong_queryset(m: MyModel, qs: QuerySet[OtherModel]) -> None:
    m.refresh_from_db(from_queryset=qs)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]


def test_meta_model(m: MyModel) -> None:
    assert_type(MyModel._meta.model, type[MyModel])
    assert_type(m._meta.model, type[MyModel])


def test_get_pk_val(m: MyModel) -> None:
    assert_type(m._get_pk_val(), Any)
    assert_type(m._get_pk_val(m._meta), Any)


def test_is_pk_set(m: MyModel) -> None:
    assert_type(m._is_pk_set(), bool)
    assert_type(m._is_pk_set(m._meta), bool)


_T = TypeVar("_T", bound=models.Model)


class GenericPkChecker(Generic[_T]):
    def check(self, m: _T) -> None:
        assert_type(m._is_pk_set(m._meta), bool)


assert_type(GenericPkChecker[MyModel]().check(MyModel()), None)
