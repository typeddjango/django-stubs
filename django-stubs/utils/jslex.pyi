from typing import Any, Dict, Iterator, List, Tuple

class Tok:
    num: int
    id: int
    name: str
    regex: str
    next: str | None
    def __init__(self, name: str, regex: str, next: str | None = ...) -> None: ...

def literals(choices: str, prefix: str = ..., suffix: str = ...) -> str: ...

class Lexer:
    regexes: Any
    toks: Dict[str, Tok]
    state: str
    def __init__(self, states: Dict[str, List[Tok]], first: str) -> None: ...
    def lex(self, text: str) -> Iterator[Tuple[str, str]]: ...

class JsLexer(Lexer):
    both_before: List[Tok]
    both_after: List[Tok]
    states: Dict[str, List[Tok]]
    def __init__(self) -> None: ...

def prepare_js_for_gettext(js: str) -> str: ...
