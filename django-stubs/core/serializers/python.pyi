from typing import Any, Dict, Iterator, List

from django.core.serializers import base
from django.core.serializers.base import DeserializedObject
from django.db.models.base import Model

class Serializer(base.Serializer):
    objects: List[Any]
    def get_dump_object(self, obj: Model) -> Dict[str, Any]: ...

def Deserializer(
    object_list: List[Dict[str, Any]], *, using: str = ..., ignorenonexistent: bool = ..., **options: Any
) -> Iterator[DeserializedObject]: ...
