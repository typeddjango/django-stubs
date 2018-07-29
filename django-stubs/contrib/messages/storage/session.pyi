from django.contrib.messages.storage.base import Message
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)


class SessionStorage:
    def __init__(self, request: HttpRequest, *args, **kwargs) -> None: ...
    def _get(
        self,
        *args,
        **kwargs
    ) -> Union[Tuple[None, bool], Tuple[List[str], bool], Tuple[List[Message], bool]]: ...
    def _store(
        self,
        messages: List[Message],
        response: HttpResponse,
        *args,
        **kwargs
    ) -> List[Any]: ...
    def deserialize_messages(
        self,
        data: Optional[str]
    ) -> Optional[Union[List[Message], List[str]]]: ...
    def serialize_messages(self, messages: Union[List[Message], List[str]]) -> str: ...