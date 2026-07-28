from __future__ import annotations

from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.validators import FileExtensionValidator
from typing_extensions import override


# Ensure subclassing narrowing the return type is allowed
class MyStorage(Storage):
    @override
    def open(self, name: str, mode: str = "rb") -> File[bytes]:
        return File(open(name, mode))


class MyValidator(FileExtensionValidator):
    @override
    def __call__(self, value: File[bytes]) -> None:
        return None
