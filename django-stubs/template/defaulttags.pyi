from datetime import date
from django.template.base import (
    FilterExpression,
    NodeList,
    Parser,
    Token,
)
from django.template.context import (
    Context,
    RequestContext,
)
from django.template.library import Library
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def autoescape(
    parser: Parser,
    token: Token
) -> AutoEscapeControlNode: ...


def comment(
    parser: Parser,
    token: Token
) -> CommentNode: ...


def csrf_token(
    parser: Parser,
    token: Token
) -> CsrfTokenNode: ...


def cycle(
    parser: Parser,
    token: Token
) -> CycleNode: ...


def do_filter(
    parser: Parser,
    token: Token
) -> FilterNode: ...


def do_for(
    parser: Parser,
    token: Token
) -> ForNode: ...


def do_if(parser: Parser, token: Token) -> IfNode: ...


def do_ifequal(
    parser: Parser,
    token: Token,
    negate: bool
) -> IfEqualNode: ...


def do_with(
    parser: Parser,
    token: Token
) -> WithNode: ...


def find_library(parser: Parser, name: str) -> Library: ...


def firstof(
    parser: Parser,
    token: Token
) -> FirstOfNode: ...


def ifchanged(
    parser: Parser,
    token: Token
) -> IfChangedNode: ...


def ifequal(
    parser: Parser,
    token: Token
) -> IfEqualNode: ...


def ifnotequal(
    parser: Parser,
    token: Token
) -> IfEqualNode: ...


def load(parser: Parser, token: Token) -> LoadNode: ...


def load_from_library(
    library: Library,
    label: str,
    names: List[str]
) -> Library: ...


def lorem(
    parser: Parser,
    token: Token
) -> LoremNode: ...


def now(parser: Parser, token: Token) -> NowNode: ...


def regroup(
    parser: Parser,
    token: Token
) -> RegroupNode: ...


def resetcycle(
    parser: Parser,
    token: Token
) -> ResetCycleNode: ...


def spaceless(
    parser: Parser,
    token: Token
) -> SpacelessNode: ...


def templatetag(
    parser: Parser,
    token: Token
) -> TemplateTagNode: ...


def url(parser: Parser, token: Token) -> URLNode: ...


def verbatim(
    parser: Parser,
    token: Token
) -> VerbatimNode: ...


def widthratio(
    parser: Parser,
    token: Token
) -> WidthRatioNode: ...


class AutoEscapeControlNode:
    def __init__(self, setting: bool, nodelist: NodeList) -> None: ...
    def render(self, context: Context) -> SafeText: ...


class CommentNode:
    def render(self, context: Context) -> str: ...


class CsrfTokenNode:
    def render(self, context: RequestContext) -> SafeText: ...


class CycleNode:
    def __init__(
        self,
        cyclevars: List[FilterExpression],
        variable_name: Optional[str] = ...,
        silent: bool = ...
    ) -> None: ...
    def render(self, context: Context) -> str: ...
    def reset(self, context: Context) -> None: ...


class FilterNode:
    def __init__(
        self,
        filter_expr: FilterExpression,
        nodelist: NodeList
    ) -> None: ...
    def render(self, context: Context): ...


class FirstOfNode:
    def __init__(self, variables: List[FilterExpression], asvar: Optional[str] = ...) -> None: ...
    def render(self, context: Context) -> str: ...


class ForNode:
    def __init__(
        self,
        loopvars: List[str],
        sequence: FilterExpression,
        is_reversed: bool,
        nodelist_loop: NodeList,
        nodelist_empty: Optional[NodeList] = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    def render(self, context: Context) -> SafeText: ...


class IfChangedNode:
    def __init__(
        self,
        nodelist_true: NodeList,
        nodelist_false: NodeList,
        *varlist
    ) -> None: ...
    def _get_context_stack_frame(self, context: Context) -> Any: ...
    def render(self, context: Context) -> str: ...


class IfEqualNode:
    def __init__(
        self,
        var1: FilterExpression,
        var2: FilterExpression,
        nodelist_true: NodeList,
        nodelist_false: NodeList,
        negate: bool
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...


class IfNode:
    def __init__(
        self,
        conditions_nodelists: Union[List[Tuple[TemplateLiteral, NodeList]], List[Union[Tuple[TemplateLiteral, NodeList], Tuple[None, NodeList]]]]
    ) -> None: ...
    def __iter__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def nodelist(self) -> NodeList: ...
    def render(self, context: Context) -> str: ...


class LoadNode:
    def render(self, context: Context) -> str: ...


class LoremNode:
    def __init__(self, count: FilterExpression, method: str, common: bool) -> None: ...
    def render(self, context: Context) -> str: ...


class NowNode:
    def __init__(self, format_string: str, asvar: None = ...) -> None: ...
    def render(self, context: Context) -> str: ...


class RegroupNode:
    def __init__(
        self,
        target: FilterExpression,
        expression: FilterExpression,
        var_name: str
    ) -> None: ...
    def render(self, context: Context) -> str: ...
    def resolve_expression(
        self,
        obj: Dict[str, Union[str, int, date, List[str]]],
        context: Context
    ) -> Union[int, str]: ...


class ResetCycleNode:
    def __init__(self, node: CycleNode) -> None: ...
    def render(self, context: Context) -> str: ...


class SpacelessNode:
    def __init__(self, nodelist: NodeList) -> None: ...
    def render(self, context: Context) -> str: ...


class TemplateIfParser:
    def __init__(self, parser: Parser, *args, **kwargs) -> None: ...
    def create_var(self, value: str) -> TemplateLiteral: ...


class TemplateLiteral:
    def __init__(self, value: FilterExpression, text: str) -> None: ...
    def display(self) -> str: ...
    def eval(self, context: Context) -> Any: ...


class TemplateTagNode:
    def __init__(self, tagtype: str) -> None: ...
    def render(self, context: Context) -> str: ...


class URLNode:
    def __init__(
        self,
        view_name: FilterExpression,
        args: List[FilterExpression],
        kwargs: Dict[str, FilterExpression],
        asvar: Optional[str]
    ) -> None: ...
    def render(self, context: Context) -> str: ...


class VerbatimNode:
    def __init__(self, content: SafeText) -> None: ...
    def render(self, context: Context) -> SafeText: ...


class WidthRatioNode:
    def __init__(
        self,
        val_expr: FilterExpression,
        max_expr: FilterExpression,
        max_width: FilterExpression,
        asvar: Optional[str] = ...
    ) -> None: ...
    def render(self, context: Context) -> str: ...


class WithNode:
    def __init__(
        self,
        var: None,
        name: None,
        nodelist: NodeList,
        extra_context: Dict[str, FilterExpression] = ...
    ) -> None: ...
    def render(self, context: Context): ...