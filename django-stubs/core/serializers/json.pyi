import json
from typing import IO, Any

from django.core.serializers.python import Deserializer as PythonDeserializer
from django.core.serializers.python import Serializer as PythonSerializer

class Serializer(PythonSerializer):
    json_kwargs: dict[str, Any]

class Deserializer(PythonDeserializer):
    def __init__(self, stream_or_string: IO[bytes] | IO[str] | bytes | str, **options: Any) -> None: ...

class DjangoJSONEncoder(json.JSONEncoder):
    allow_nan: bool
    check_circular: bool
    ensure_ascii: bool
    indent: int
    skipkeys: bool
    sort_keys: bool
