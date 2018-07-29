from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.checks.messages import Error
from django.core.files.storage import (
    DefaultStorage,
    FileSystemStorage,
)
from typing import (
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)


def find(path: str, all: bool = ...) -> Optional[str]: ...


def get_finder(import_path: str) -> BaseFinder: ...


def get_finders() -> Iterator[BaseFinder]: ...


class AppDirectoriesFinder:
    def __init__(self, app_names: None = ..., *args, **kwargs) -> None: ...
    def find(self, path: str, all: bool = ...) -> str: ...
    def find_in_app(self, app: str, path: str) -> Optional[str]: ...
    def list(self, ignore_patterns: List[str]) -> Iterator[Tuple[str, FileSystemStorage]]: ...


class BaseFinder:
    def check(self, **kwargs): ...


class BaseStorageFinder:
    def __init__(
        self,
        storage: Optional[StaticFilesStorage] = ...,
        *args,
        **kwargs
    ) -> None: ...
    def list(self, ignore_patterns: List[str]) -> Iterator[Tuple[str, DefaultStorage]]: ...


class DefaultStorageFinder:
    def __init__(self, *args, **kwargs) -> None: ...


class FileSystemFinder:
    def __init__(self, app_names: None = ..., *args, **kwargs) -> None: ...
    def check(self, **kwargs) -> List[Error]: ...
    def find(self, path: str, all: bool = ...) -> Union[str, List[str]]: ...
    def find_location(self, root: str, path: str, prefix: str = ...) -> Optional[str]: ...
    def list(self, ignore_patterns: List[str]) -> Iterator[Tuple[str, FileSystemStorage]]: ...