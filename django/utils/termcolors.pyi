from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
    Union,
)


def colorize(text: str = ..., opts: Union[str, Tuple] = ..., **kwargs) -> str: ...


def make_style(opts: Tuple = ..., **kwargs) -> Callable: ...


def parse_color_setting(
    config_string: str
) -> Optional[Union[Dict[str, Dict[str, str]], Dict[str, Dict[str, Union[str, Tuple[str]]]]]]: ...