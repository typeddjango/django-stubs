from typing import (
    Callable,
    List,
    Optional,
    Union,
)


def check_errors(fn: Callable) -> Callable: ...


def clean_files(filelist: Union[List[Union[None, bool]], List[str], List[Union[None, str]]]) -> List[str]: ...


def gen_filenames(only_new: bool = ...) -> List[str]: ...


def reset_translations() -> None: ...