from django.apps.registry import Apps
from django.core.checks.messages import (
    Error,
    Warning,
)
from typing import (
    Any,
    List,
    Optional,
    Set,
    Tuple,
)


def _check_lazy_references(
    apps: Apps,
    ignore: Optional[Set[Tuple[str, str]]] = ...
) -> List[Error]: ...


def check_all_models(app_configs: None = ..., **kwargs) -> List[Warning]: ...


def check_lazy_references(app_configs: None = ..., **kwargs) -> List[Any]: ...