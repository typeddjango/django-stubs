from typing import Any, Optional

from django.db.models.query_utils import RegisterLookupMixin


class Field(RegisterLookupMixin):
    def __init__(self,
                 primary_key: bool = False,
                 **kwargs): ...

    def __get__(self, instance, owner) -> Any: ...


class IntegerField(Field):
    def __get__(self, instance, owner) -> int: ...


class SmallIntegerField(IntegerField): ...


class BigIntegerField(IntegerField): ...


class AutoField(Field):
    def __get__(self, instance, owner) -> int: ...


class CharField(Field):
    def __init__(self,
                 max_length: int,
                 **kwargs): ...

    def __get__(self, instance, owner) -> str: ...


class SlugField(CharField): ...


class TextField(Field):
    def __get__(self, instance, owner) -> str: ...


class BooleanField(Field):
    def __get__(self, instance, owner) -> bool: ...


class FileField(Field): ...


class IPAddressField(Field): ...


class GenericIPAddressField(Field):
    default_error_messages: Any = ...
    unpack_ipv4: Any = ...
    protocol: Any = ...

    def __init__(
            self,
            verbose_name: Optional[Any] = ...,
            name: Optional[Any] = ...,
            protocol: str = ...,
            unpack_ipv4: bool = ...,
            *args: Any,
            **kwargs: Any
    ) -> None: ...

class DateField(Field): ...

class DateTimeField(DateField): ...