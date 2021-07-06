from typing import Any

from .utils.version import get_version as get_version

VERSION: Any
__version__: str

def setup(set_prefix: bool = ...) -> None: ...

# Used internally by mypy_django_plugin.
class _AnyAttrAllowed:
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, item: str, value: Any) -> None: ...
