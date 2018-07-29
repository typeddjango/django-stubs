from django.apps.config import AppConfig
from django.apps.registry import Apps
from django.contrib.contenttypes.models import ContentType
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps
from typing import (
    Any,
    Type,
)


def create_contenttypes(
    app_config: AppConfig,
    verbosity: int = ...,
    interactive: bool = ...,
    using: str = ...,
    apps: Apps = ...,
    **kwargs
) -> None: ...


def get_contenttypes_and_models(
    app_config: AppConfig,
    using: str,
    ContentType: Type[ContentType]
) -> Any: ...


def inject_rename_contenttypes_operations(
    plan: Any = ...,
    apps: StateApps = ...,
    using: str = ...,
    **kwargs
) -> None: ...


class RenameContentType:
    def __init__(self, app_label: str, old_model: str, new_model: str) -> None: ...
    def _rename(
        self,
        apps: StateApps,
        schema_editor: DatabaseSchemaEditor,
        old_model: str,
        new_model: str
    ) -> None: ...
    def rename_backward(
        self,
        apps: StateApps,
        schema_editor: DatabaseSchemaEditor
    ) -> None: ...
    def rename_forward(
        self,
        apps: StateApps,
        schema_editor: DatabaseSchemaEditor
    ) -> None: ...