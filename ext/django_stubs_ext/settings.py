from pathlib import Path
from typing import Any, TypedDict, type_check_only

from typing_extensions import NotRequired


@type_check_only
class TemplatesSetting(TypedDict):
    """Typing helper if you want to type `TEMPLATE` setting."""

    BACKEND: str
    NAME: NotRequired[str]
    DIRS: NotRequired[list[str | Path]]
    APP_DIRS: NotRequired[bool]
    OPTIONS: NotRequired[dict[str, Any]]


__all__ = ["TemplatesSetting"]
