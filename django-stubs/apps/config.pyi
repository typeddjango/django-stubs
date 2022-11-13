import types
from collections.abc import Iterator

from django.apps.registry import Apps
from django.db.models.base import Model
from django.utils.functional import _StrOrPromise

MODELS_MODULE_NAME: str

class AppConfig:
    name: str
    module: types.ModuleType | None
    apps: Apps | None
    label: str
    verbose_name: _StrOrPromise
    path: str
    models_module: str | None
    models: dict[str, type[Model]]
    def __init__(self, app_name: str, app_module: types.ModuleType | None) -> None: ...
    @classmethod
    def create(cls, entry: str) -> AppConfig: ...
    def get_model(self, model_name: str, require_ready: bool = ...) -> type[Model]: ...
    def get_models(self, include_auto_created: bool = ..., include_swapped: bool = ...) -> Iterator[type[Model]]: ...
    def import_models(self) -> None: ...
    def ready(self) -> None: ...
