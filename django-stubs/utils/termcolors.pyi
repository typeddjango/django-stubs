from typing import Any, Callable, Dict, Mapping, Sequence, Tuple

color_names: Sequence
foreground: Mapping[str, str]
background: Mapping[str, str]
RESET: str
opt_dict: Mapping[str, str]

def colorize(text: str | None = ..., opts: Sequence[str] = ..., **kwargs: Any) -> str: ...
def make_style(opts: Tuple = ..., **kwargs: Any) -> Callable: ...

NOCOLOR_PALETTE: str
DARK_PALETTE: str
LIGHT_PALETTE: str
PALETTES: Any
DEFAULT_PALETTE: str

def parse_color_setting(config_string: str) -> Dict[str, Dict[str, Tuple[str, ...] | str]] | None: ...
