from django.db.models.base import Model
from typing import Optional


class FieldCacheMixin:
    def delete_cached_value(self, instance: Model) -> None: ...
    def get_cached_value(
        self,
        instance: Model,
        default: object = ...
    ) -> Optional[Model]: ...
    def is_cached(self, instance: Model) -> bool: ...
    def set_cached_value(
        self,
        instance: Model,
        value: Optional[Model]
    ) -> None: ...