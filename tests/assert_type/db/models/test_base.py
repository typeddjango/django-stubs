from collections.abc import Iterable

from django.db import models
from django.db.models.query import QuerySet
from typing_extensions import override


class MyModel(models.Model):
    @override
    def refresh_from_db(
        self,
        using: str | None = None,
        fields: Iterable[str] | None = None,
        from_queryset: QuerySet[models.Model] | None = None,
    ) -> None: ...

    class Meta:
        app_label = "myapp"
