from collections.abc import Callable, Collection, Iterable, Mapping, Sequence, Sized
from typing import Any, Literal, TypeVar, overload

from django.template.base import FilterExpression, Origin, Parser, Token
from django.template.context import Context
from django.utils.safestring import SafeString
from typing_extensions import Concatenate

from .base import Node, Template

class InvalidTemplateLibrary(Exception): ...

_C = TypeVar("_C", bound=Callable[..., Any])
_CompileC = TypeVar("_CompileC", bound=Callable[[Parser, Token], Node])
_FilterC = TypeVar("_FilterC", bound=Callable[[Any], Any] | Callable[[Any, Any], Any])
_TakesContextC = TypeVar("_TakesContextC", bound=Callable[Concatenate[Context, ...], Any])

class Library:
    filters: dict[str, Callable[[Any], Any] | Callable[[Any, Any], Any]]
    tags: dict[str, Callable[[Parser, Token], Node]]
    def __init__(self) -> None: ...
    # @register.tag
    @overload
    def tag(self, name: _CompileC, /) -> _CompileC: ...
    # register.tag("somename", somefunc)
    @overload
    def tag(self, name: str, compile_function: _CompileC) -> _CompileC: ...
    # @register.tag()
    # @register.tag("somename") or @register.tag(name="somename")
    @overload
    def tag(self, name: str | None = ..., compile_function: None = ...) -> Callable[[_CompileC], _CompileC]: ...
    def tag_function(self, func: _CompileC) -> _CompileC: ...
    # @register.filter
    @overload
    def filter(self, name: _FilterC, /) -> _FilterC: ...
    # @register.filter()
    # @register.filter("somename") or @register.filter(name='somename')
    @overload
    def filter(
        self,
        *,
        name: str | None = ...,
        filter_func: None = ...,
        is_safe: bool = ...,
        needs_autoescape: bool = ...,
        expects_localtime: bool = ...,
    ) -> Callable[[_FilterC], _FilterC]: ...
    # register.filter("somename", somefunc)
    @overload
    def filter(
        self,
        name: str,
        filter_func: _FilterC,
        *,
        is_safe: bool = ...,
        needs_autoescape: bool = ...,
        expects_localtime: bool = ...,
    ) -> _FilterC: ...
    # @register.simple_tag
    @overload
    def simple_tag(self, func: _C, /) -> _C: ...
    # @register.simple_tag(takes_context=True)
    @overload
    def simple_tag(
        self, *, takes_context: Literal[True], name: str | None = ...
    ) -> Callable[[_TakesContextC], _TakesContextC]: ...
    # @register.simple_tag(takes_context=False)
    # @register.simple_tag(...)
    @overload
    def simple_tag(
        self, *, takes_context: Literal[False] | None = ..., name: str | None = ...
    ) -> Callable[[_C], _C]: ...
    @overload
    def inclusion_tag(
        self,
        filename: Template | str,
        func: Callable[..., Any] | None = ...,
        *,
        takes_context: Literal[True],
        name: str | None = ...,
    ) -> Callable[[_TakesContextC], _TakesContextC]: ...
    @overload
    def inclusion_tag(
        self,
        filename: Template | str,
        func: Callable[..., Any] | None = ...,
        takes_context: Literal[False] | None = ...,
        name: str | None = ...,
    ) -> Callable[[_C], _C]: ...

class TagHelperNode(Node):
    func: Any
    takes_context: Any
    args: Any
    kwargs: Any
    def __init__(
        self,
        func: Callable,
        takes_context: bool | None,
        args: list[FilterExpression],
        kwargs: dict[str, FilterExpression],
    ) -> None: ...
    def get_resolved_arguments(self, context: Context) -> tuple[list[int], dict[str, SafeString | int]]: ...

class SimpleNode(TagHelperNode):
    args: list[FilterExpression]
    func: Callable
    kwargs: dict[str, FilterExpression]
    origin: Origin
    takes_context: bool | None
    token: Token
    target_var: str | None
    def __init__(
        self,
        func: Callable,
        takes_context: bool | None,
        args: list[FilterExpression],
        kwargs: dict[str, FilterExpression],
        target_var: str | None,
    ) -> None: ...

class InclusionNode(TagHelperNode):
    args: list[FilterExpression]
    func: Callable
    kwargs: dict[str, FilterExpression]
    origin: Origin
    takes_context: bool | None
    token: Token
    filename: Template | str
    def __init__(
        self,
        func: Callable,
        takes_context: bool | None,
        args: list[FilterExpression],
        kwargs: dict[str, FilterExpression],
        filename: Template | str | None,
    ) -> None: ...

def parse_bits(
    parser: Parser,
    bits: Iterable[str],
    params: Sequence[str],
    varargs: str | None,
    varkw: str | None,
    defaults: Sized | None,
    kwonly: Collection[str],
    kwonly_defaults: Mapping[str, int] | None,
    takes_context: bool | None,
    name: str,
) -> tuple[list[FilterExpression], dict[str, FilterExpression]]: ...
def import_library(name: str) -> Library: ...
