from typing import Any

from django.apps import AppConfig

class SitesConfig(AppConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    path: str
    name: str = ...
    verbose_name: Any = ...
    def ready(self) -> None: ...
