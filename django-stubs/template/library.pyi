from django.template.base import (
    FilterExpression,
    Parser,
    Template,
)
from django.template.context import Context
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


def import_library(name: str) -> Library: ...


def parse_bits(
    parser: Parser,
    bits: List[str],
    params: List[str],
    varargs: Optional[str],
    varkw: None,
    defaults: Optional[Union[Tuple[bool, None], Tuple[str]]],
    kwonly: List[str],
    kwonly_defaults: Optional[Dict[str, int]],
    takes_context: Optional[bool],
    name: str
) -> Union[Tuple[List[Any], Dict[Any, Any]], Tuple[List[FilterExpression], Dict[str, FilterExpression]], Tuple[List[Any], Dict[str, FilterExpression]], Tuple[List[FilterExpression], Dict[Any, Any]]]: ...


class InclusionNode:
    def __init__(
        self,
        func: Callable,
        takes_context: Optional[bool],
        args: List[FilterExpression],
        kwargs: Dict[Any, Any],
        filename: Optional[Union[str, Template]]
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...


class Library:
    def __init__(self) -> None: ...
    def filter(
        self,
        name: Optional[Union[str, Callable]] = ...,
        filter_func: Optional[Callable] = ...,
        **flags
    ) -> Callable: ...
    def filter_function(self, func: Callable, **flags) -> Callable: ...
    def inclusion_tag(
        self,
        filename: Union[str, Template],
        func: None = ...,
        takes_context: Optional[bool] = ...,
        name: Optional[str] = ...
    ) -> Callable: ...
    def simple_tag(
        self,
        func: Optional[Callable] = ...,
        takes_context: Optional[bool] = ...,
        name: Optional[str] = ...
    ) -> Callable: ...
    def tag(
        self,
        name: Optional[Union[str, Callable]] = ...,
        compile_function: Optional[Union[str, Callable]] = ...
    ) -> Callable: ...
    def tag_function(self, func: Callable) -> Callable: ...


class SimpleNode:
    def __init__(
        self,
        func: Callable,
        takes_context: Optional[bool],
        args: List[FilterExpression],
        kwargs: Dict[str, FilterExpression],
        target_var: Optional[str]
    ) -> None: ...
    def render(self, context: Context) -> str: ...


class TagHelperNode:
    def __init__(
        self,
        func: Callable,
        takes_context: Optional[bool],
        args: List[FilterExpression],
        kwargs: Dict[Any, Any]
    ) -> None: ...
    def get_resolved_arguments(self, context: Context) -> Any: ...