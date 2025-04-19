from typing import IO, Any

from django.core.serializers.python import Deserializer as PythonDeserializer
from django.core.serializers.python import Serializer as PythonSerializer

class Serializer(PythonSerializer):
    json_kwargs: dict[str, Any]

class Deserializer(PythonDeserializer):
    def __init__(self, stream_or_string: IO[bytes] | IO[str] | bytes | str, **options: Any) -> None: ...
