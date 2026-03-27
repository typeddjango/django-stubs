from typing import ClassVar

from django.db import migrations
from django.db.migrations.operations.base import Operation


class ExplicitMigration(migrations.Migration):
    operations: ClassVar[list[Operation]] = []  # pyright: ignore[reportIncompatibleVariableOverride]
    initial: ClassVar[bool] = True  # pyright: ignore[reportIncompatibleVariableOverride]


# Non-ClassVar annotations are incorrect
class ExplicitIncorrectMigration(migrations.Migration):
    operations: list[Operation] = []  # type: ignore[misc]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
    initial: bool = True  # type: ignore[misc]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


class ImplicitMigration(migrations.Migration):
    operations = []
    initial = True
