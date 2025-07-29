from django.contrib.staticfiles.storage import ConfiguredStorage, StaticFilesStorage, staticfiles_storage
from typing_extensions import assert_type

# The plugin can figure out what these are (but pyright can't):
assert_type(staticfiles_storage, StaticFilesStorage)  # pyright: ignore[reportAssertTypeFailure]

# what pyright thinks these are:
assert_type(staticfiles_storage, ConfiguredStorage)  # mypy: ignore[assert-type]
