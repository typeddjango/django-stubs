from re import Pattern

dot_re: Pattern[str]

def blankout(src: str, char: str) -> str: ...

context_re: Pattern[str]
inline_re: Pattern[str]
block_re: Pattern[str]
endblock_re: Pattern[str]
plural_re: Pattern[str]
constant_re: Pattern[str]

def templatize(src: str, origin: str = ...) -> str: ...
