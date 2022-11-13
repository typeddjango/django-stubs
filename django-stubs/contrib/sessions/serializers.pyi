from django.core.signing import JSONSerializer as BaseJSONSerializer
from django.db.models.base import Model

class PickleSerializer:
    def dumps(self, obj: dict[str, Model]) -> bytes: ...
    def loads(self, data: bytes) -> dict[str, Model]: ...

JSONSerializer = BaseJSONSerializer
