from logging import Logger
from typing import Any

logger: Logger
lib_path: str
lib_names: list[str]
lgdal: Any
lwingdal: Any

def std_call(func: Any) -> Any: ...
def gdal_version() -> bytes: ...
def gdal_full_version() -> bytes: ...
def gdal_version_info() -> tuple[int, int, int]: ...

GDAL_VERSION: tuple[int, int, int]
CPLErrorHandler: Any

def err_handler(error_class: Any, error_number: Any, message: Any) -> None: ...
def function(name: Any, args: Any, restype: Any) -> Any: ...

set_error_handler: Any
