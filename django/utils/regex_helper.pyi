from typing import (
    Any,
    Iterator,
    List,
    Tuple,
    Type,
    Union,
)


def contains(
    source: Union[str, Group, NonCapture],
    inst: Type[Group]
) -> bool: ...


def flatten_result(source: Any) -> Union[Tuple[List[str], List[List[str]]], Tuple[List[str], List[List[Any]]]]: ...


def get_quantifier(ch: str, input_iter: Iterator[Any]) -> Union[Tuple[int, None], Tuple[int, str]]: ...


def normalize(
    pattern: str
) -> Union[List[Tuple[str, List[Any]]], List[Union[Tuple[str, List[Any]], Tuple[str, List[str]]]], List[Tuple[str, List[str]]]]: ...


def walk_to_end(ch: str, input_iter: Iterator[Any]) -> None: ...