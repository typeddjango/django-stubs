from django.template.base import (
    Origin,
    Template,
)
from django.template.library import Library
from django.template.loaders.base import Loader
from django.template.loaders.cached import Loader
from django.template.loaders.filesystem import Loader
from django.template.loaders.locmem import Loader
from django.utils.safestring import SafeText
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class Engine:
    def __init__(
        self,
        dirs: Optional[List[str]] = ...,
        app_dirs: bool = ...,
        context_processors: Optional[Union[List[str], Tuple[str, str]]] = ...,
        debug: bool = ...,
        loaders: Any = ...,
        string_if_invalid: str = ...,
        file_charset: str = ...,
        libraries: Optional[Dict[str, str]] = ...,
        builtins: Optional[List[str]] = ...,
        autoescape: bool = ...
    ) -> None: ...
    def find_template(
        self,
        name: str,
        dirs: None = ...,
        skip: Optional[List[Origin]] = ...
    ) -> Tuple[Template, Origin]: ...
    def find_template_loader(
        self,
        loader: Union[Tuple[str, List[Tuple[str, Dict[str, str]]]], Tuple[str, List[str]], Tuple[str, Dict[str, str]], str]
    ) -> Loader: ...
    def from_string(self, template_code: str) -> Template: ...
    @staticmethod
    def get_default() -> Engine: ...
    def get_template(self, template_name: str) -> Template: ...
    def get_template_builtins(self, builtins: List[str]) -> List[Library]: ...
    def get_template_libraries(self, libraries: Dict[str, str]) -> Dict[str, Library]: ...
    def get_template_loaders(self, template_loaders: Any) -> Any: ...
    def render_to_string(self, template_name: str, context: Any = ...) -> SafeText: ...
    def select_template(self, template_name_list: List[str]) -> Template: ...
    @cached_property
    def template_context_processors(
        self
    ) -> Union[Tuple[Callable, Callable, Callable], Tuple[Callable], Tuple[Callable, Callable, Callable, Callable, Callable], Tuple[Callable, Callable]]: ...
    @cached_property
    def template_loaders(
        self
    ) -> Union[List[Loader], List[Loader], List[Loader]]: ...