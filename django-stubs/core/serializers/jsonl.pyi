from typing import Any, Dict, IO, Iterator, Union

from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.base import DeserializedObject

class Serializer(PythonSerializer):
    json_kwargs: Dict[str, Any]

def Deserializer(stream_or_string: Union[IO[bytes], IO[str], bytes, str], **options: Any) -> Iterator[DeserializedObject]: ...
