from django.core.files.storage import (
    DefaultStorage,
    FileSystemStorage,
)
from django.core.management.base import CommandParser
from typing import (
    Dict,
    List,
    Optional,
    Union,
)


class Command:
    def __init__(self, *args, **kwargs) -> None: ...
    def add_arguments(self, parser: CommandParser) -> None: ...
    def clear_dir(self, path: str) -> None: ...
    def collect(self) -> Dict[str, List[str]]: ...
    def copy_file(
        self,
        path: str,
        prefixed_path: str,
        source_storage: Union[FileSystemStorage, DefaultStorage]
    ) -> None: ...
    def delete_file(
        self,
        path: str,
        prefixed_path: str,
        source_storage: Union[FileSystemStorage, DefaultStorage]
    ) -> bool: ...
    def handle(self, **options) -> Optional[str]: ...
    def is_local_storage(self) -> bool: ...
    def link_file(
        self,
        path: str,
        prefixed_path: str,
        source_storage: Union[FileSystemStorage, DefaultStorage]
    ) -> None: ...
    @cached_property
    def local(self) -> bool: ...
    def log(self, msg: str, level: int = ...) -> None: ...
    def set_options(self, **options) -> None: ...