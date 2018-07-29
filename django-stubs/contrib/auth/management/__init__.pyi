from django.apps.config import AppConfig
from django.apps.registry import Apps
from django.db.models.options import Options
from typing import (
    List,
    Tuple,
)


def _get_all_permissions(opts: Options) -> List[Tuple[str, str]]: ...


def _get_builtin_permissions(opts: Options) -> List[Tuple[str, str]]: ...


def create_permissions(
    app_config: AppConfig,
    verbosity: int = ...,
    interactive: bool = ...,
    using: str = ...,
    apps: Apps = ...,
    **kwargs
) -> None: ...


def get_default_username(check_db: bool = ...) -> str: ...


def get_system_username() -> str: ...