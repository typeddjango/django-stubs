from typing import Any, Optional

from django.apps import AppConfig

from .management import create_contenttypes, inject_rename_contenttypes_operations

class ContentTypesConfig(AppConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    path: str
    name: str = ...
    verbose_name: Any = ...
    def ready(self) -> None: ...
