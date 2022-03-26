import json
from typing import IO, Any, Dict, Iterator, Union

from django.core.serializers.base import DeserializedObject
from django.core.serializers.python import Serializer as PythonSerializer

class Serializer(PythonSerializer):
    json_kwargs: Dict[str, Any]

def Deserializer(
    stream_or_string: Union[IO[bytes], IO[str], bytes, str], **options: Any
) -> Iterator[DeserializedObject]: ...

class DjangoJSONEncoder(json.JSONEncoder):
    allow_nan: bool
    check_circular: bool
    ensure_ascii: bool
    indent: int
    skipkeys: bool
    sort_keys: bool
