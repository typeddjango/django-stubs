from __future__ import annotations

from typing import ClassVar

from django.db import migrations


class ExplicitMigration(migrations.Migration):
    initial: ClassVar[bool] = True  # pyright: ignore[reportIncompatibleVariableOverride]  # ty: ignore[invalid-mutable-override]


# initial remains a class-only default.
class IncorrectInitialMigration(migrations.Migration):
    initial: bool = True  # type: ignore[misc]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-attribute-override]


class ImplicitMigration(migrations.Migration):
    operations = []
    initial = True


migration = ImplicitMigration("migration", "app")
migration.operations = []
migration.dependencies = [("app", "migration")]
migration.run_before = [("app", "migration")]
migration.replaces = [("app", "migration")]
