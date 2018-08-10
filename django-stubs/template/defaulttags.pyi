from collections import namedtuple
from datetime import date, time
from decimal import Decimal
from sqlite3 import OperationalError
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from django.contrib.admin.helpers import ActionForm, AdminForm
from django.contrib.auth.context_processors import PermLookupDict, PermWrapper
from django.contrib.messages.storage.base import BaseStorage
from django.core.exceptions import FieldDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.fields import AutoField
from django.db.models.query import QuerySet
from django.forms.boundfield import BoundField
from django.template.base import FilterExpression, NodeList, Parser, Token
from django.template.context import Context, RequestContext
from django.template.exceptions import TemplateDoesNotExist
from django.template.library import Library
from django.urls.resolvers import URLPattern, URLResolver
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import SafeText

from .base import (BLOCK_TAG_END, BLOCK_TAG_START, COMMENT_TAG_END,
                   COMMENT_TAG_START, FILTER_SEPARATOR, SINGLE_BRACE_END,
                   SINGLE_BRACE_START, VARIABLE_ATTRIBUTE_SEPARATOR,
                   VARIABLE_TAG_END, VARIABLE_TAG_START, Context, Node,
                   NodeList, TemplateSyntaxError, VariableDoesNotExist,
                   kwarg_re, render_value_in_context, token_kwargs)
from .defaultfilters import date
from .library import Library
from .smartif import IfParser, Literal

register: Any

class AutoEscapeControlNode(Node):
    nodelist: django.template.base.NodeList
    origin: django.template.base.Origin
    setting: bool
    token: django.template.base.Token
    def __init__(self, setting: bool, nodelist: NodeList) -> None: ...
    def render(self, context: Context) -> SafeText: ...

class CommentNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    def render(self, context: Context) -> str: ...

class CsrfTokenNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    def render(self, context: RequestContext) -> SafeText: ...

class CycleNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    cyclevars: List[django.template.base.FilterExpression] = ...
    variable_name: Optional[str] = ...
    silent: bool = ...
    def __init__(
        self,
        cyclevars: List[FilterExpression],
        variable_name: Optional[str] = ...,
        silent: bool = ...,
    ) -> None: ...
    def render(self, context: Context) -> str: ...
    def reset(self, context: Context) -> None: ...

class DebugNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    def render(self, context: Context) -> str: ...

class FilterNode(Node):
    filter_expr: django.template.base.FilterExpression
    nodelist: django.template.base.NodeList
    origin: django.template.base.Origin
    token: django.template.base.Token
    def __init__(
        self, filter_expr: FilterExpression, nodelist: NodeList
    ) -> None: ...
    def render(self, context: Context) -> Any: ...

class FirstOfNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    vars: List[django.template.base.FilterExpression] = ...
    asvar: Optional[str] = ...
    def __init__(
        self, variables: List[FilterExpression], asvar: Optional[str] = ...
    ) -> None: ...
    def render(self, context: Context) -> str: ...

class ForNode(Node):
    loopvars: Union[List[str], str]
    origin: django.template.base.Origin
    sequence: Union[django.template.base.FilterExpression, str]
    token: django.template.base.Token
    child_nodelists: Any = ...
    is_reversed: bool = ...
    nodelist_loop: List[str] = ...
    nodelist_empty: List[str] = ...
    def __init__(
        self,
        loopvars: Union[List[str], str],
        sequence: Union[FilterExpression, str],
        is_reversed: bool,
        nodelist_loop: List[str],
        nodelist_empty: Optional[List[str]] = ...,
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...

class IfChangedNode(Node):
    nodelist_false: django.template.base.NodeList
    nodelist_true: django.template.base.NodeList
    origin: django.template.base.Origin
    token: django.template.base.Token
    child_nodelists: Any = ...
    def __init__(
        self, nodelist_true: NodeList, nodelist_false: NodeList, *varlist: Any
    ) -> None: ...
    def render(self, context: Context) -> str: ...

class IfEqualNode(Node):
    nodelist_false: List[Any]
    nodelist_true: List[Any]
    origin: django.template.base.Origin
    token: django.template.base.Token
    var1: Union[django.template.base.FilterExpression, str]
    var2: Union[django.template.base.FilterExpression, str]
    child_nodelists: Any = ...
    negate: bool = ...
    def __init__(
        self,
        var1: Union[FilterExpression, str],
        var2: Union[FilterExpression, str],
        nodelist_true: List[Any],
        nodelist_false: List[Any],
        negate: bool,
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...

class IfNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    conditions_nodelists: List[
        Union[
            Tuple[None, django.template.base.NodeList],
            Tuple[
                django.template.defaulttags.TemplateLiteral,
                django.template.base.NodeList,
            ],
        ]
    ] = ...
    def __init__(
        self,
        conditions_nodelists: List[
            Union[Tuple[None, NodeList], Tuple[TemplateLiteral, NodeList]]
        ],
    ) -> None: ...
    def __iter__(self) -> None: ...
    @property
    def nodelist(self) -> NodeList: ...
    def render(self, context: Context) -> str: ...

class LoremNode(Node):
    common: bool
    count: django.template.base.FilterExpression
    method: str
    origin: django.template.base.Origin
    token: django.template.base.Token
    def __init__(
        self, count: FilterExpression, method: str, common: bool
    ) -> None: ...
    def render(self, context: Context) -> str: ...

GroupedResult = namedtuple("GroupedResult", ["grouper", "list"])

class RegroupNode(Node):
    expression: django.template.base.FilterExpression
    origin: django.template.base.Origin
    target: django.template.base.FilterExpression
    token: django.template.base.Token
    var_name: str = ...
    def __init__(
        self,
        target: FilterExpression,
        expression: FilterExpression,
        var_name: str,
    ) -> None: ...
    def resolve_expression(
        self,
        obj: Union[
            Dict[str, Union[List[str], str]],
            Dict[str, Union[int, str]],
            Dict[str, date],
        ],
        context: Context,
    ) -> Union[int, str]: ...
    def render(self, context: Context) -> str: ...

class LoadNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    def render(self, context: Context) -> str: ...

class NowNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    format_string: str = ...
    asvar: Optional[str] = ...
    def __init__(
        self, format_string: str, asvar: Optional[str] = ...
    ) -> None: ...
    def render(self, context: Context) -> str: ...

class ResetCycleNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    node: django.template.defaulttags.CycleNode = ...
    def __init__(self, node: CycleNode) -> None: ...
    def render(self, context: Context) -> str: ...

class SpacelessNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    nodelist: django.template.base.NodeList = ...
    def __init__(self, nodelist: NodeList) -> None: ...
    def render(self, context: Context) -> str: ...

class TemplateTagNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    mapping: Any = ...
    tagtype: str = ...
    def __init__(self, tagtype: str) -> None: ...
    def render(self, context: Context) -> str: ...

class URLNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    view_name: django.template.base.FilterExpression = ...
    args: List[django.template.base.FilterExpression] = ...
    kwargs: Dict[str, django.template.base.FilterExpression] = ...
    asvar: Optional[str] = ...
    def __init__(
        self,
        view_name: FilterExpression,
        args: List[FilterExpression],
        kwargs: Dict[str, FilterExpression],
        asvar: Optional[str],
    ) -> None: ...
    def render(self, context: Context) -> str: ...

class VerbatimNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    content: django.utils.safestring.SafeText = ...
    def __init__(self, content: SafeText) -> None: ...
    def render(self, context: Context) -> SafeText: ...

class WidthRatioNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    val_expr: django.template.base.FilterExpression = ...
    max_expr: django.template.base.FilterExpression = ...
    max_width: django.template.base.FilterExpression = ...
    asvar: Optional[str] = ...
    def __init__(
        self,
        val_expr: FilterExpression,
        max_expr: FilterExpression,
        max_width: FilterExpression,
        asvar: Optional[str] = ...,
    ) -> None: ...
    def render(self, context: Context) -> str: ...

class WithNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    nodelist: List[Any] = ...
    extra_context: Union[
        Dict[str, django.template.base.FilterExpression], Dict[str, str]
    ] = ...
    def __init__(
        self,
        var: Optional[str],
        name: Optional[str],
        nodelist: List[Any],
        extra_context: Optional[Dict[str, FilterExpression]] = ...,
    ) -> None: ...
    def render(self, context: Context) -> Any: ...

def autoescape(parser: Parser, token: Token) -> AutoEscapeControlNode: ...
def comment(parser: Parser, token: Token) -> CommentNode: ...
def cycle(parser: Parser, token: Token) -> CycleNode: ...
def csrf_token(parser: Parser, token: Token) -> CsrfTokenNode: ...
def debug(parser: Parser, token: Token) -> DebugNode: ...
def do_filter(parser: Parser, token: Token) -> FilterNode: ...
def firstof(parser: Parser, token: Token) -> FirstOfNode: ...
def do_for(parser: Parser, token: Token) -> ForNode: ...
def do_ifequal(parser: Parser, token: Token, negate: bool) -> IfEqualNode: ...
def ifequal(parser: Parser, token: Token) -> IfEqualNode: ...
def ifnotequal(parser: Parser, token: Token) -> IfEqualNode: ...

class TemplateLiteral(Literal):
    value: django.template.base.FilterExpression = ...
    text: str = ...
    def __init__(self, value: FilterExpression, text: str) -> None: ...
    def display(self) -> str: ...
    def eval(
        self, context: Context
    ) -> Optional[
        Union[
            AttributeError,
            Dict[str, Union[List[Tuple[int, SafeText]], int, str]],
            KeyError,
            List[List[Union[URLPattern, URLResolver]]],
            List[Tuple[str, str]],
            List[
                Union[
                    Dict[str, Union[List[Any], str]],
                    Dict[
                        str, Union[List[Dict[str, Union[List[Any], str]]], str]
                    ],
                ]
            ],
            List[BoundField],
            List[TemplateDoesNotExist],
            List[int],
            List[str],
            Set[Any],
            Tuple,
            TypeError,
            date,
            time,
            Decimal,
            ActionForm,
            AdminForm,
            PermLookupDict,
            PermWrapper,
            BaseStorage,
            FieldDoesNotExist,
            WSGIRequest,
            Model,
            AutoField,
            QuerySet,
            MultiValueDict,
            float,
            int,
            OperationalError,
            str,
        ]
    ]: ...

class TemplateIfParser(IfParser):
    current_token: django.template.defaulttags.TemplateLiteral
    pos: int
    tokens: List[django.template.defaulttags.TemplateLiteral]
    error_class: Any = ...
    template_parser: django.template.base.Parser = ...
    def __init__(self, parser: Parser, *args: Any, **kwargs: Any) -> None: ...
    def create_var(self, value: str) -> TemplateLiteral: ...

def do_if(parser: Parser, token: Token) -> IfNode: ...
def ifchanged(parser: Parser, token: Token) -> IfChangedNode: ...
def find_library(parser: Parser, name: str) -> Library: ...
def load_from_library(
    library: Library, label: str, names: List[str]
) -> Library: ...
def load(parser: Parser, token: Token) -> LoadNode: ...
def lorem(parser: Parser, token: Token) -> LoremNode: ...
def now(parser: Parser, token: Token) -> NowNode: ...
def regroup(parser: Parser, token: Token) -> RegroupNode: ...
def resetcycle(parser: Parser, token: Token) -> ResetCycleNode: ...
def spaceless(parser: Parser, token: Token) -> SpacelessNode: ...
def templatetag(parser: Parser, token: Token) -> TemplateTagNode: ...
def url(parser: Parser, token: Token) -> URLNode: ...
def verbatim(parser: Parser, token: Token) -> VerbatimNode: ...
def widthratio(parser: Parser, token: Token) -> WidthRatioNode: ...
def do_with(parser: Parser, token: Token) -> WithNode: ...
