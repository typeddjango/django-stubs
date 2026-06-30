from __future__ import annotations

from django.urls import register_converter
from django.urls.converters import IntConverter

# Builtin converter
register_converter(IntConverter, "bigint")


# Custom converter
class BigIntConverter:
    regex = r"[0-9]+"

    def to_python(self, value: str) -> int:
        return int(value)

    def to_url(self, value: int) -> str:
        return str(value)


register_converter(BigIntConverter, "bigint")


# Incorrect types: to_python must accept str, to_url must return str
class BadConverter:
    regex = r"[0-9]+"

    def to_python(self, value: int) -> str:
        return str(value)

    def to_url(self, value: str) -> int:
        return int(value)


register_converter(BadConverter, "bigint")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]
