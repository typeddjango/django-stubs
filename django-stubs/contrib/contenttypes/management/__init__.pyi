from typing import Dict, List, Optional, Tuple, Type, Union

from django.apps.config import AppConfig
from django.apps.registry import Apps
from django.contrib.admin.migrations.0001_initial import Migration
from django.contrib.admin.migrations.0002_logentry_remove_auto_add import \
    Migration
from django.contrib.admin.migrations.0003_logentry_add_action_flag_choices import \
    Migration
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.migrations.0001_initial import Migration
from django.contrib.sites.migrations.0002_alter_domain_unique import Migration
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.migration import Migration
from django.db.migrations.state import StateApps
from django.db.models.base import Model


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
) -> Tuple[Dict[str, ContentType], Dict[str, Type[Model]]]: ...


def inject_rename_contenttypes_operations(
    plan: List[Union[Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool]]] = ...,
    apps: StateApps = ...,
    using: str = ...,
    **kwargs
) -> None: ...


class RenameContentType:
    def __init__(self, app_label: str, old_model: str, new_model: str) -> None: ...
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
