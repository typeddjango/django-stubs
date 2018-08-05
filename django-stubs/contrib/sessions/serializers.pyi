from datetime import datetime
from typing import Any, Dict, Optional, Union

from django.core.signing import JSONSerializer as BaseJSONSerializer
from django.db.models.base import Model


class PickleSerializer:
    def dumps(self, obj: Dict[str, Union[Model, str, datetime]]) -> bytes: ...
    def loads(self, data: bytes) -> Dict[str, Union[Model, str, datetime]]: ...

JSONSerializer = BaseJSONSerializer
