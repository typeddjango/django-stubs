from hmac import HMAC
from typing import Any, Callable, Optional, Union

using_sysrandom: bool

def salted_hmac(
    key_salt: str,
    value: Union[str, bytes],
    secret: Optional[Union[str, bytes]] = ...,
) -> HMAC: ...
def get_random_string(length: int = ..., allowed_chars: str = ...) -> str: ...
def constant_time_compare(
    val1: Union[str, bytes], val2: Union[str, bytes]
) -> bool: ...
def pbkdf2(
    password: Union[str, bytes],
    salt: Union[str, bytes],
    iterations: int,
    dklen: int = ...,
    digest: Optional[Callable] = ...,
) -> bytes: ...
