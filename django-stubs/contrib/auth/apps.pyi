from typing import Any, Optional

from django.apps import AppConfig

from .checks import check_models_permissions, check_user_model
from .management import create_permissions
from .signals import user_logged_in

class AuthConfig(AppConfig):
    apps: None
    label: str
    models: None
    models_module: None
    module: Any
    path: str
    name: str = ...
    verbose_name: Any = ...
    def ready(self) -> None: ...
