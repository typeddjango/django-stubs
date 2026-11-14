from collections.abc import Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage, Warning

W001: Warning

def check_gdal_39(app_configs: Sequence[AppConfig] | None, **kwargs: object) -> list[CheckMessage]: ...
