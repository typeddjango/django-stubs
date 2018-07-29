from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)


def literals(choices: str, prefix: str = ..., suffix: str = ...) -> str: ...


def prepare_js_for_gettext(js: str) -> str: ...


class JsLexer:
    def __init__(self) -> None: ...


class Lexer:
    def __init__(self, states: Dict[str, List[Tok]], first: str) -> None: ...
    def lex(self, text: str) -> Iterator[Tuple[str, str]]: ...


class Tok:
    def __init__(self, name: str, regex: str, next: Optional[str] = ...) -> None: ...