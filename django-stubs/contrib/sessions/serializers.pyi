from datetime import datetime
from django.db.models.base import Model
from typing import (
    Dict,
    Union,
)


class PickleSerializer:
    def dumps(self, obj: Dict[str, Union[str, datetime]]) -> bytes: ...
    def loads(self, data: bytes) -> Dict[str, Model]: ...