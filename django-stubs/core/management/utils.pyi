from django.db.models.base import Model
from typing import (
    Any,
    List,
    Set,
    Tuple,
    Type,
    Union,
)


def find_command(cmd: str, path: None = ..., pathext: None = ...) -> str: ...


def handle_extensions(extensions: List[str]) -> Set[str]: ...


def parse_apps_and_model_labels(
    labels: List[str]
) -> Union[Tuple[Set[Type[Model]], Set[Any]], Tuple[Set[Any], Set[Any]]]: ...


def popen_wrapper(args: List[str], stdout_encoding: str = ...) -> Tuple[str, str, int]: ...