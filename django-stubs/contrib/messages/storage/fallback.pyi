from typing import Any, Optional

from django.contrib.messages.storage.base import BaseStorage

class FallbackStorage(BaseStorage):
    added_new: bool
    request: WSGIRequest
    used: bool
    storage_classes: Any = ...
    storages: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
