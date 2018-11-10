from typing import List, Any, TypeVar, Generic

from django.contrib.postgres.fields.mixins import CheckFieldDefaultMixin
from django.db.models import Field

_T = TypeVar('_T', bound=Field)


class ArrayField(CheckFieldDefaultMixin, Field, Generic[_T]):
    def __init__(self,
                 base_field: Field,
                 **kwargs): ...

    def __get__(self, instance, owner) -> List[_T]: ...
