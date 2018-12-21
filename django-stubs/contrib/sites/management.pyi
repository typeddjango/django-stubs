from typing import Any

from django.apps.registry import Apps
from django.contrib.sites.apps import SitesConfig

def create_default_site(
    app_config: SitesConfig,
    verbosity: int = ...,
    interactive: bool = ...,
    using: str = ...,
    apps: Apps = ...,
    **kwargs: Any
) -> None: ...
