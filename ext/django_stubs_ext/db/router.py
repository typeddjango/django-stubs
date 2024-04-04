from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from typing import Any

    from django.db.models import Model

    class TypedDatabaseRouter:
        """
        Typed base class for Django's DATABASE_ROUTERS setting. At runtime this is just an alias to `object`.

        All methods are optional.

        Django documentation: https://docs.djangoproject.com/en/stable/topics/db/multi-db/#automatic-database-routing
        """

        def db_for_read(self, model: Type[Model], **hints: Any) -> Optional[str]: ...

        def db_for_write(self, model: Type[Model], **hints: Any) -> Optional[str]: ...

        def allow_relation(self, obj1: Type[Model], obj2: Type[Model], **hints: Any) -> Optional[bool]: ...

        def allow_migrate(
            self, db: str, app_label: str, model_name: Optional[str] = None, **hints: Any
        ) -> Optional[bool]: ...

else:
    TypedDatabaseRouter = object
