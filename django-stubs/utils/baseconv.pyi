from typing import Tuple, Union

BASE2_ALPHABET: str
BASE16_ALPHABET: str
BASE56_ALPHABET: str
BASE36_ALPHABET: str
BASE62_ALPHABET: str
BASE64_ALPHABET: str

class BaseConverter:
    decimal_digits: str = ...
    sign: str = ...
    digits: str = ...
    def __init__(self, digits: str, sign: str = ...) -> None: ...
    def encode(self, i: int) -> str: ...
    def decode(self, s: str) -> int: ...
    def convert(self, number: Union[int, str], from_digits: str, to_digits: str, sign: str) -> Tuple[int, str]: ...

base2: BaseConverter
base16: BaseConverter
base36: BaseConverter
base56: BaseConverter
base62: BaseConverter
base64: BaseConverter
