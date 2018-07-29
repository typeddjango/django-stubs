from datetime import datetime
from django.contrib.sessions.serializers import PickleSerializer
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)


def b64_decode(s: bytes) -> bytes: ...


def b64_encode(s: bytes) -> bytes: ...


def base64_hmac(salt: str, value: Union[str, bytes], key: Union[str, bytes]) -> str: ...


def dumps(
    obj: Union[str, List[str], Dict[str, Union[str, datetime]], Dict[str, str]],
    key: None = ...,
    salt: str = ...,
    serializer: Type[Union[PickleSerializer, JSONSerializer]] = ...,
    compress: bool = ...
) -> str: ...


def get_cookie_signer(salt: str = ...) -> TimestampSigner: ...


def loads(
    s: str,
    key: None = ...,
    salt: str = ...,
    serializer: Type[Union[PickleSerializer, JSONSerializer]] = ...,
    max_age: Optional[int] = ...
) -> Union[str, List[str], Dict[str, str]]: ...


class JSONSerializer:
    def dumps(self, obj: Any) -> bytes: ...
    def loads(self, data: bytes) -> Union[List[str], Dict[str, str]]: ...


class Signer:
    def __init__(
        self,
        key: Optional[Union[str, bytes]] = ...,
        sep: str = ...,
        salt: Optional[str] = ...
    ) -> None: ...
    def sign(self, value: str) -> str: ...
    def signature(self, value: Union[str, bytes]) -> str: ...
    def unsign(self, signed_value: str) -> str: ...


class TimestampSigner:
    def sign(self, value: str) -> str: ...
    def timestamp(self) -> str: ...
    def unsign(self, value: str, max_age: Optional[int] = ...) -> str: ...