from django.contrib.auth.models import User
from django.db.models.base import Model
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Type,
    Union,
)


class LazyObject:
    def __delattr__(self, name: str) -> None: ...
    def __init__(self) -> None: ...
    def __reduce__(
        self
    ) -> Union[Tuple[Callable, Tuple[object]], Tuple[Callable, Tuple[User]], Tuple[Callable, Tuple[Model]]]: ...
    def __setattr__(self, name: str, value: object) -> None: ...


class SimpleLazyObject:
    def __copy__(self) -> object: ...
    def __deepcopy__(self, memo: Dict[Any, Any]) -> List[int]: ...
    def __init__(self, func: Callable) -> None: ...
    def _setup(self) -> None: ...


class cached_property:
    def __get__(self, instance: Any, cls: Type[Any] = ...) -> Any: ...