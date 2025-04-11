from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from django.db.models import Model

    class TypedDatabaseRouter:
        """
        Typed base class for Django's DATABASE_ROUTERS setting. At runtime this is just an alias to `object`.

        All methods are optional.

        Django documentation: https://docs.djangoproject.com/en/stable/topics/db/multi-db/#automatic-database-routing
        """

        def db_for_read(self, model: type[Model], **hints: Any) -> str | None: ...

        def db_for_write(self, model: type[Model], **hints: Any) -> str | None: ...

        def allow_relation(self, obj1: type[Model], obj2: type[Model], **hints: Any) -> bool | None: ...

        def allow_migrate(
            self, db: str, app_label: str, model_name: str | None = None, **hints: Any
        ) -> bool | None: ...

else:
    TypedDatabaseRouter = object
