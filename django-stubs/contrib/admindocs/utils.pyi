from typing import Callable


def get_view_name(view_func: Callable) -> str: ...


def replace_named_groups(pattern: str) -> str: ...


def replace_unnamed_groups(pattern: str) -> str: ...