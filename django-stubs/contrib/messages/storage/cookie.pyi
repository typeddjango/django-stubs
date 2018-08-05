import json
from typing import Any, Collection, Dict, List, Optional, Union

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
    def default(self, obj: Message) -> List[Union[str, int]]: ...

class MessageDecoder(json.JSONDecoder):
    def process_messages(self, obj: Collection) -> Any: ...
    def decode(
        self, s: str, **kwargs: Any
    ) -> Union[
        List[
            Union[
                Dict[
                    str,
                    Union[Message, List[Union[Message, Dict[str, Message]]]],
                ],
                Message,
            ]
        ],
        Message,
        List[Union[Message, str]],
    ]: ...

class CookieStorage(BaseStorage):
    added_new: bool
    request: django.core.handlers.wsgi.WSGIRequest
    used: bool
    cookie_name: str = ...
    max_cookie_size: int = ...
    not_finished: str = ...
