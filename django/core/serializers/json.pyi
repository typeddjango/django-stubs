from datetime import (
    date,
    timedelta,
)
from decimal import Decimal
from django.db.models.base import Model
from typing import (
    Any,
    Optional,
    Union,
)
from uuid import UUID


def Deserializer(stream_or_string: Any, **options) -> None: ...


class DjangoJSONEncoder:
    def default(self, o: Union[Decimal, UUID, date, timedelta]) -> str: ...


class Serializer:
    def _init_options(self) -> None: ...
    def end_object(self, obj: Model) -> None: ...
    def end_serialization(self) -> None: ...
    def getvalue(self) -> Optional[str]: ...
    def start_serialization(self) -> None: ...