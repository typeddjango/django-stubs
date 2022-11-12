from enum import Enum
from logging import Logger
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Pattern, Sequence, Tuple, Type

from django.template.context import Context as Context
from django.template.engine import Engine
from django.template.library import Library
from django.template.loaders.base import Loader
from django.utils.safestring import SafeString

FILTER_SEPARATOR: str
FILTER_ARGUMENT_SEPARATOR: str
VARIABLE_ATTRIBUTE_SEPARATOR: str
BLOCK_TAG_START: str
BLOCK_TAG_END: str
VARIABLE_TAG_START: str
VARIABLE_TAG_END: str
COMMENT_TAG_START: str
COMMENT_TAG_END: str
TRANSLATOR_COMMENT_MARK: str
SINGLE_BRACE_START: str
SINGLE_BRACE_END: str
UNKNOWN_SOURCE: str
tag_re: Pattern[str]
logger: Logger

class TokenType(Enum):
    TEXT: int
    VAR: int
    BLOCK: int
    COMMENT: int

class VariableDoesNotExist(Exception):
    msg: str
    params: Tuple[Dict[str, str] | str]
    def __init__(self, msg: str, params: Tuple[Dict[str, str] | str] = ...) -> None: ...

class Origin:
    name: str
    template_name: bytes | str | None
    loader: Loader | None
    def __init__(self, name: str, template_name: bytes | str | None = ..., loader: Loader | None = ...) -> None: ...
    @property
    def loader_name(self) -> str | None: ...

class Template:
    name: str | None
    origin: Origin
    engine: Engine
    source: str
    nodelist: NodeList
    def __init__(
        self,
        template_string: Template | str,
        origin: Origin | None = ...,
        name: str | None = ...,
        engine: Engine | None = ...,
    ) -> None: ...
    def __iter__(self) -> Iterator[Node]: ...
    def render(self, context: Context | Dict[str, Any] | None) -> SafeString: ...
    def compile_nodelist(self) -> NodeList: ...
    def get_exception_info(self, exception: Exception, token: Token) -> Dict[str, Any]: ...

def linebreak_iter(template_source: str) -> Iterator[int]: ...

class Token:
    contents: str
    token_type: TokenType
    lineno: int | None
    position: Tuple[int, int] | None
    def __init__(
        self,
        token_type: TokenType,
        contents: str,
        position: Tuple[int, int] | None = ...,
        lineno: int | None = ...,
    ) -> None: ...
    def split_contents(self) -> List[str]: ...

class Lexer:
    template_string: str
    verbatim: bool | str
    def __init__(self, template_string: str) -> None: ...
    def tokenize(self) -> List[Token]: ...
    def create_token(self, token_string: str, position: Tuple[int, int] | None, lineno: int, in_tag: bool) -> Token: ...

class DebugLexer(Lexer):
    template_string: str
    verbatim: bool | str
    def tokenize(self) -> List[Token]: ...

class Parser:
    tokens: List[Token] | str
    tags: Dict[str, Callable]
    filters: Dict[str, Callable]
    command_stack: List[Tuple[str, Token]]
    libraries: Dict[str, Library]
    origin: Origin | None
    def __init__(
        self,
        tokens: List[Token] | str,
        libraries: Dict[str, Library] | None = ...,
        builtins: List[Library] | None = ...,
        origin: Origin | None = ...,
    ) -> None: ...
    def parse(self, parse_until: Iterable[str] | None = ...) -> NodeList: ...
    def skip_past(self, endtag: str) -> None: ...
    def extend_nodelist(self, nodelist: NodeList, node: Node, token: Token) -> None: ...
    def error(self, token: Token, e: Exception | str) -> Exception: ...
    def invalid_block_tag(self, token: Token, command: str, parse_until: Iterable[str] | None = ...) -> Any: ...
    def unclosed_block_tag(self, parse_until: Iterable[str]) -> Any: ...
    def next_token(self) -> Token: ...
    def prepend_token(self, token: Token) -> None: ...
    def delete_first_token(self) -> None: ...
    def add_library(self, lib: Library) -> None: ...
    def compile_filter(self, token: str) -> FilterExpression: ...
    def find_filter(self, filter_name: str) -> Callable: ...

constant_string: str
filter_raw_string: str
filter_re: Pattern[str]

class FilterExpression:
    token: str
    filters: List[Any]
    var: Any
    def __init__(self, token: str, parser: Parser) -> None: ...
    def resolve(self, context: Context, ignore_failures: bool = ...) -> Any: ...
    @staticmethod
    def args_check(name: str, func: Callable, provided: List[Tuple[bool, Any]]) -> bool: ...

class Variable:
    var: Dict[Any, Any] | str
    literal: SafeString | float | None
    lookups: Tuple[str] | None
    translate: bool
    message_context: str | None
    def __init__(self, var: Dict[Any, Any] | str) -> None: ...
    def resolve(self, context: Mapping[str, Mapping[str, Any]] | Context | int | str) -> Any: ...

class Node:
    must_be_first: bool
    child_nodelists: Any
    origin: Origin
    token: Token | None
    def render(self, context: Context) -> str: ...
    def render_annotated(self, context: Context) -> int | str: ...
    def __iter__(self) -> Iterator[Node]: ...
    def get_nodes_by_type(self, nodetype: Type[Node]) -> List[Node]: ...

class NodeList(List[Node]):
    contains_nontext: bool
    def render(self, context: Context) -> SafeString: ...
    def get_nodes_by_type(self, nodetype: Type[Node]) -> List[Node]: ...

class TextNode(Node):
    s: str
    def __init__(self, s: str) -> None: ...

def render_value_in_context(value: Any, context: Context) -> str: ...

class VariableNode(Node):
    filter_expression: FilterExpression
    def __init__(self, filter_expression: FilterExpression) -> None: ...

kwarg_re: Pattern[str]

def token_kwargs(bits: Sequence[str], parser: Parser, support_legacy: bool = ...) -> Dict[str, FilterExpression]: ...
