from collections.abc import Callable, Mapping, Sequence
from typing import Any

color_names: Sequence
foreground: Mapping[str, str]
background: Mapping[str, str]
RESET: str
opt_dict: Mapping[str, str]

def colorize(text: str | None = ..., opts: Sequence[str] = ..., **kwargs: Any) -> str: ...
def make_style(opts: tuple = ..., **kwargs: Any) -> Callable: ...

NOCOLOR_PALETTE: str
DARK_PALETTE: str
LIGHT_PALETTE: str
PALETTES: Any
DEFAULT_PALETTE: str

def parse_color_setting(config_string: str) -> dict[str, dict[str, tuple[str, ...] | str]] | None: ...
