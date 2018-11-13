from typing import Any

from django.db.models.query_utils import RegisterLookupMixin


class Field(RegisterLookupMixin):
    def __init__(self,
                 primary_key: bool = False,
                 **kwargs): ...
    def __get__(self, instance, owner) -> Any: ...


class IntegerField(Field):
    def __get__(self, instance, owner) -> int: ...


class SmallIntegerField(IntegerField):
    pass


class AutoField(Field):
    def __get__(self, instance, owner) -> int: ...


class CharField(Field):
    def __init__(self,
                 max_length: int,
                 **kwargs): ...
    def __get__(self, instance, owner) -> str: ...


class SlugField(CharField):
    pass


class TextField(Field):
    def __get__(self, instance, owner) -> str: ...


class BooleanField(Field):
    def __get__(self, instance, owner) -> bool: ...
