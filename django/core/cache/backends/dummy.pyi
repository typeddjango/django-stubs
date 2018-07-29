from typing import (
    Any,
    Dict,
    Optional,
    Union,
)


class DummyCache:
    def __init__(self, host: str, *args, **kwargs) -> None: ...
    def add(self, key: str, value: str, timeout: object = ..., version: None = ...) -> bool: ...
    def get(self, key: str, default: Optional[str] = ..., version: Optional[int] = ...) -> Optional[str]: ...
    def has_key(self, key: str, version: None = ...) -> bool: ...
    def set(
        self,
        key: str,
        value: Union[str, int, Dict[str, Any]],
        timeout: object = ...,
        version: Optional[str] = ...
    ) -> None: ...