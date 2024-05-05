from typing import Any

from django.contrib.messages.storage.base import Message
from django.http.response import HttpResponse

class MessagesTestMixin:
    def assertMessages(
        self, response: HttpResponse, expected_messages: list[dict[str, Any] | type[Message]], *, ordered: bool = ...
    ) -> None: ...
