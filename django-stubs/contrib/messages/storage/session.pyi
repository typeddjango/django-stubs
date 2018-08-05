from typing import Any, List, Optional, Union

from django.contrib.messages.storage.base import BaseStorage, Message
from django.http.request import HttpRequest


class SessionStorage(BaseStorage):
    added_new: bool
    request: django.core.handlers.wsgi.WSGIRequest
    used: bool
    session_key: str = ...
    def __init__(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> None: ...
    def serialize_messages(
        self, messages: Union[List[Message], List[str]]
    ) -> str: ...
    def deserialize_messages(
        self, data: Optional[Union[str, List[Any]]]
    ) -> Optional[Union[List[str], List[Message]]]: ...
