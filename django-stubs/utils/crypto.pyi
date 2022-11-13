from collections.abc import Callable
from hmac import HMAC

using_sysrandom: bool
RANDOM_STRING_CHARS: str

def salted_hmac(
    key_salt: bytes | str, value: bytes | str, secret: bytes | str | None = ..., *, algorithm: str = ...
) -> HMAC: ...
def get_random_string(length: int = ..., allowed_chars: str = ...) -> str: ...
def constant_time_compare(val1: bytes | str, val2: bytes | str) -> bool: ...
def pbkdf2(
    password: bytes | str,
    salt: bytes | str,
    iterations: int,
    dklen: int = ...,
    digest: Callable | None = ...,
) -> bytes: ...
