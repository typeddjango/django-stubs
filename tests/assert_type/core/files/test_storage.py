from django.core.files.storage import DefaultStorage, FileSystemStorage, Storage, default_storage, storages
from typing_extensions import assert_type

# The plugin can figure out what these are (but pyright can't):
assert_type(default_storage, FileSystemStorage)  # pyright: ignore[reportAssertTypeFailure]
assert_type(storages["default"], FileSystemStorage)  # pyright: ignore[reportAssertTypeFailure]

# what pyright thinks these are:
assert_type(default_storage, DefaultStorage)  # mypy: ignore[assert-type]
assert_type(storages["default"], Storage)  # mypy: ignore[assert-type]
