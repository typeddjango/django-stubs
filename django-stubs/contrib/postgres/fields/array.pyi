from typing import List, Any

from django.contrib.postgres.fields.mixins import CheckFieldDefaultMixin
from django.db.models import Field


class ArrayField(CheckFieldDefaultMixin, Field):
    def __init__(self,
                 base_field: Field,
                 **kwargs): ...
    def __get__(self, instance, owner) -> List[Any]: ...