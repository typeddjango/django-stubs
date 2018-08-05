from typing import Any, Callable, Dict, Optional, Tuple, Union

color_names: Any
foreground: Any
background: Any
RESET: str
opt_dict: Any

def colorize(
    text: Optional[str] = ..., opts: Union[str, Tuple] = ..., **kwargs: Any
) -> str: ...
def make_style(opts: Tuple = ..., **kwargs: Any) -> Callable: ...

NOCOLOR_PALETTE: str
DARK_PALETTE: str
LIGHT_PALETTE: str
PALETTES: Any
DEFAULT_PALETTE = DARK_PALETTE

def parse_color_setting(
    config_string: str
) -> Optional[
    Union[
        Dict[str, Dict[str, Union[str, Tuple[str]]]],
        Dict[str, Dict[str, Union[str, Tuple[str, str]]]],
    ]
]: ...
