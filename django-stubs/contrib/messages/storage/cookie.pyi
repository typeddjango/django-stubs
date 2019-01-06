import json
from typing import Any, Dict, List, Optional, Union

from django.contrib.messages.storage.base import BaseStorage, Message

class MessageEncoder(json.JSONEncoder):
    allow_nan: bool
    check_circular: bool
    ensure_ascii: bool
    indent: None
    item_separator: str
    key_separator: str
    skipkeys: bool
    sort_keys: bool
    message_key: str = ...
    def default(self, obj: Message) -> List[Union[int, str]]: ...

class MessageDecoder(json.JSONDecoder):
    def process_messages(
        self,
        obj: Union[
            Dict[
                str, Union[List[Union[Dict[str, List[Union[int, str]]], List[Union[int, str]]]], List[Union[int, str]]]
            ],
            List[Union[List[Union[int, str]], str]],
            str,
        ],
    ) -> Union[
        Dict[str, Union[List[Union[Dict[str, Message], Message]], Message]],
        List[Union[Dict[str, Union[List[Union[Dict[str, Message], Message]], Message]], Message]],
        List[Union[Message, str]],
        Message,
        str,
    ]: ...
    def decode(
        self, s: str, **kwargs: Any
    ) -> Union[
        List[Union[Dict[str, Union[List[Union[Dict[str, Message], Message]], Message]], Message]],
        List[Union[Message, str]],
        Message,
    ]: ...

class CookieStorage(BaseStorage):
    added_new: bool
    request: WSGIRequest
    used: bool
    cookie_name: str = ...
    max_cookie_size: int = ...
    not_finished: str = ...
