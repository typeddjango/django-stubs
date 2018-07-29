from django.contrib.messages.storage.base import Message
from django.http.response import HttpResponse
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)


class CookieStorage:
    def _decode(self, data: Optional[str]) -> Any: ...
    def _encode(
        self,
        messages: Union[List[str], List[Message]],
        encode_empty: bool = ...
    ) -> Optional[str]: ...
    def _get(
        self,
        *args,
        **kwargs
    ) -> Union[Tuple[None, bool], Tuple[List[str], bool], Tuple[List[Any], bool], Tuple[List[Message], bool]]: ...
    def _hash(self, value: str) -> str: ...
    def _store(
        self,
        messages: List[Message],
        response: HttpResponse,
        remove_oldest: bool = ...,
        *args,
        **kwargs
    ) -> List[Message]: ...
    def _update_cookie(self, encoded_data: Optional[str], response: HttpResponse) -> None: ...


class MessageDecoder:
    def decode(
        self,
        s: str,
        **kwargs
    ) -> Union[List[Message], List[Union[Message, str]], List[str]]: ...
    def process_messages(self, obj: Any) -> Any: ...


class MessageEncoder:
    def default(self, obj: Message) -> List[Union[int, str]]: ...