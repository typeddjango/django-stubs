from collections.abc import Iterable

from django.db import models
from django.db.models.query import QuerySet
from typing_extensions import assert_type, override


class MyModel(models.Model):
    class Meta:
        app_label = "myapp"


class OtherModel(models.Model):
    class Meta:
        app_label = "myapp"


# Override with QuerySet[Model] — valid
class OverrideWithModel(models.Model):
    @override
    def refresh_from_db(
        self,
        using: str | None = None,
        fields: Iterable[str] | None = None,
        from_queryset: QuerySet[models.Model] | None = None,
    ) -> None: ...

    class Meta:
        app_label = "myapp"


def test_correct_queryset(m: MyModel, qs: QuerySet[MyModel]) -> None:
    m.refresh_from_db(from_queryset=qs)
    assert_type(m.refresh_from_db(), None)


def test_wrong_queryset(m: MyModel, qs: QuerySet[OtherModel]) -> None:
    m.refresh_from_db(from_queryset=qs)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]
