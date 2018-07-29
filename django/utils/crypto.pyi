from hmac import HMAC
from typing import (
    Callable,
    Optional,
    Union,
)


def constant_time_compare(val1: Union[str, bytes], val2: Union[str, bytes]) -> bool: ...


def get_random_string(length: int = ..., allowed_chars: str = ...) -> str: ...


def pbkdf2(password: str, salt: str, iterations: int, dklen: int = ..., digest: Callable = ...) -> bytes: ...


def salted_hmac(key_salt: str, value: Union[str, bytes], secret: Optional[Union[str, bytes]] = ...) -> HMAC: ...