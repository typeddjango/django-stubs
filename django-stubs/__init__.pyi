from typing import Any
from .utils.version import get_version as get_version

VERSION: Any
__version__: str

def setup(set_prefix: bool = ...) -> None: ...

# Used by mypy_django_plugin on an annotated Model returned by a QuerySet where .annotate was called
# (e.g. where field names are unknown)
class _AnyAttrAllowed:
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, item: str, value: Any) -> None: ...
