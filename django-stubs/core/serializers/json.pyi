import json
from datetime import datetime
from decimal import Decimal
from io import TextIOWrapper
from typing import Any, Optional, Union, Dict, Type
from uuid import UUID

from django.core.serializers.python import Serializer as PythonSerializer
from django.db.models.base import Model

class Serializer(PythonSerializer):
    json_kwargs: Dict[str, Optional[Type[DjangoJSONEncoder]]]
    options: Dict[str, None]
    selected_fields: None
    stream: TextIOWrapper
    use_natural_foreign_keys: bool
    use_natural_primary_keys: bool
    internal_use_only: bool = ...
    def start_serialization(self) -> None: ...
    def end_serialization(self) -> None: ...
    def end_object(self, obj: Model) -> None: ...
    def getvalue(self) -> Optional[Union[bytes, str]]: ...

def Deserializer(stream_or_string: Any, **options: Any) -> None: ...

class DjangoJSONEncoder(json.JSONEncoder):
    allow_nan: bool
    check_circular: bool
    ensure_ascii: bool
    indent: None
    skipkeys: bool
    sort_keys: bool
    def default(self, o: Union[datetime, Decimal, UUID]) -> str: ...
