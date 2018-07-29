from django.template.base import (
    FilterExpression,
    NodeList,
    Parser,
    Template,
    Token,
)
from django.template.context import Context
from django.utils.safestring import SafeText
from typing import (
    Dict,
    Optional,
)


def construct_relative_path(current_template_name: Optional[str], relative_name: str) -> str: ...


def do_block(
    parser: Parser,
    token: Token
) -> BlockNode: ...


def do_extends(
    parser: Parser,
    token: Token
) -> ExtendsNode: ...


def do_include(
    parser: Parser,
    token: Token
) -> IncludeNode: ...


class BlockContext:
    def __init__(self) -> None: ...
    def add_blocks(self, blocks: Dict[str, BlockNode]) -> None: ...
    def get_block(self, name: str) -> BlockNode: ...
    def pop(self, name: str) -> BlockNode: ...
    def push(self, name: str, block: BlockNode) -> None: ...


class BlockNode:
    def __init__(self, name: str, nodelist: NodeList, parent: None = ...) -> None: ...
    def __repr__(self) -> str: ...
    def render(self, context: Context) -> SafeText: ...
    def super(self) -> SafeText: ...


class ExtendsNode:
    def __init__(
        self,
        nodelist: NodeList,
        parent_name: FilterExpression,
        template_dirs: None = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    def find_template(
        self,
        template_name: str,
        context: Context
    ) -> Template: ...
    def get_parent(self, context: Context) -> Template: ...
    def render(self, context: Context): ...


class IncludeNode:
    def __init__(
        self,
        template: FilterExpression,
        *args,
        extra_context = ...,
        isolated_context = ...,
        **kwargs
    ) -> None: ...
    def render(self, context: Context) -> SafeText: ...