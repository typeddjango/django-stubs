from __future__ import annotations

from typing import Any

from django.contrib.messages.storage.cookie import MessageDecoder
from typing_extensions import assert_type


def test_process_messages_return_type() -> None:
    decoder = MessageDecoder()

    result = decoder.process_messages("test_string")
    assert_type(result, Any)

    list_result = decoder.process_messages([])
    assert_type(list_result, Any)
