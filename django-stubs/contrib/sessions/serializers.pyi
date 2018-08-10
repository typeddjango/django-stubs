from datetime import datetime
from typing import Any, Dict, Optional, Union

from django.core.signing import JSONSerializer as BaseJSONSerializer
from django.db.models.base import Model


class PickleSerializer:
    def dumps(
        self, obj: Union[Dict[str, Union[datetime, str]], Dict[str, Model]]
    ) -> bytes: ...
    def loads(
        self, data: bytes
    ) -> Union[Dict[str, Union[datetime, str]], Dict[str, Model]]: ...

JSONSerializer = BaseJSONSerializer
