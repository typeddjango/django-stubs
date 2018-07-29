from typing import (
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
)


class BaseEngine:
    def __init__(self, params: Dict[str, Union[str, bool, List[str]]]) -> None: ...
    def iter_template_filenames(self, template_name: str) -> Iterator[str]: ...
    @cached_property
    def template_dirs(self) -> Tuple: ...