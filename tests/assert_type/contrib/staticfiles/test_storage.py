from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.staticfiles.storage import HashedFilesMixin
from typing_extensions import override

if TYPE_CHECKING:
    from django.core.files.base import File


# Ensure subclassing narrowing the content arg in contravariant position is allowed
class ZulipStorage(HashedFilesMixin):
    @override
    def hashed_name(self, name: str, content: File[bytes] | None = None, filename: str | None = None) -> str:
        return name

    @override
    def file_hash(self, name: str, content: File[bytes] | None = None) -> str | None:
        return None
