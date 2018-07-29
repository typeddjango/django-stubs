from django.contrib.messages.storage.base import Message
from django.http.response import HttpResponse
from typing import (
    Any,
    List,
    Tuple,
    Union,
)


class FallbackStorage:
    def __init__(self, *args, **kwargs) -> None: ...
    def _get(
        self,
        *args,
        **kwargs
    ) -> Union[Tuple[List[Any], bool], Tuple[List[str], bool], Tuple[List[Message], bool]]: ...
    def _store(
        self,
        messages: List[Message],
        response: HttpResponse,
        *args,
        **kwargs
    ) -> List[Any]: ...