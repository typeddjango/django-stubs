from typing import Set, Tuple

from django.db.migrations.serializer import BaseSerializer as BaseSerializer

class RangeSerializer(BaseSerializer):
    def serialize(self) -> Tuple[str, Set[str]]: ...
