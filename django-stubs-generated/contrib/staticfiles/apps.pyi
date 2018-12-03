from typing import Any, Optional

from django.apps import AppConfig

class StaticFilesConfig(AppConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    path: str
    name: str = ...
    verbose_name: Any = ...
    ignore_patterns: Any = ...
    def ready(self) -> None: ...
