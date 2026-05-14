from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.db import migrations

if TYPE_CHECKING:
    from django.db.migrations.operations.base import Operation


class ExplicitMigration(migrations.Migration):
    operations: ClassVar[list[Operation]] = []  # pyright: ignore[reportIncompatibleVariableOverride]
    initial: ClassVar[bool] = True  # pyright: ignore[reportIncompatibleVariableOverride]


# Non-ClassVar annotations are incorrect
class ExplicitIncorrectMigration(migrations.Migration):
    operations: list[Operation] = []  # type: ignore[misc]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-attribute-override]
    initial: bool = True  # type: ignore[misc]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-attribute-override]


class ImplicitMigration(migrations.Migration):
    operations = []
    initial = True
