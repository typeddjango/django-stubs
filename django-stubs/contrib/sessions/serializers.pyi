from django.core.signing import JSONSerializer as BaseJSONSerializer
from django.db.models.base import Model
from typing_extensions import TypeAlias

class PickleSerializer:
    def dumps(self, obj: dict[str, Model]) -> bytes: ...
    def loads(self, data: bytes) -> dict[str, Model]: ...

JSONSerializer: TypeAlias = BaseJSONSerializer
