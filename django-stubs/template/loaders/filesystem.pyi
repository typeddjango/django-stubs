from django.template.base import Origin
from django.template.engine import Engine
from typing import (
    Iterator,
    List,
    Union,
)


class Loader:
    def __init__(self, engine: Engine, dirs: None = ...) -> None: ...
    def get_contents(self, origin: Origin): ...
    def get_dirs(self) -> List[str]: ...
    def get_template_sources(self, template_name: Union[bytes, str]) -> Iterator[Origin]: ...