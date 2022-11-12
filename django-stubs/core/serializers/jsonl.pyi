from typing import IO, Any, Dict, Iterator

from django.core.serializers.base import DeserializedObject
from django.core.serializers.python import Serializer as PythonSerializer

class Serializer(PythonSerializer):
    json_kwargs: Dict[str, Any]

def Deserializer(
    stream_or_string: IO[bytes] | IO[str] | bytes | str, **options: Any
) -> Iterator[DeserializedObject]: ...
