from typing import Any

from django.core.serializers import base
from django.db.models.base import Model

class Serializer(base.Serializer):
    objects: list[Any]
    def get_dump_object(self, obj: Model) -> dict[str, Any]: ...

class Deserializer(base.Deserializer):
    def __init__(
        self, object_list: list[dict[str, Any]], *, using: str = ..., ignorenonexistent: bool = False, **options: Any
    ) -> None: ...
