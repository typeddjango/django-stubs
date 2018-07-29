from typing import (
    Callable,
    List,
)


def func_accepts_kwargs(func: Callable) -> bool: ...


def func_accepts_var_args(func: Callable) -> bool: ...


def func_supports_parameter(func: Callable, parameter: str) -> bool: ...


def get_func_args(func: Callable) -> List[str]: ...