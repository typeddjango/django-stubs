from typing import Any

from django.apps import AppConfig

class SimpleAdminConfig(AppConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    path: str
    default_site: str = ...
    name: str = ...
    verbose_name: Any = ...
    def ready(self) -> None: ...

class AdminConfig(SimpleAdminConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    name: str
    path: str
    def ready(self) -> None: ...
