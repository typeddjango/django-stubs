from typing import (
    Tuple,
    Union,
)


class BaseConverter:
    def convert(self, number: Union[str, int], from_digits: str, to_digits: str, sign: str) -> Tuple[int, str]: ...
    def decode(self, s: str) -> int: ...
    def encode(self, i: int) -> str: ...