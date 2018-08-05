from typing import Any, Dict, List, Optional, Union

from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages.storage.session import SessionStorage
from django.http.request import HttpRequest


def messages(
    request: HttpRequest
) -> Dict[
    str,
    Union[
        List[Any],
        Dict[str, int],
        FallbackStorage,
        SessionStorage,
        CookieStorage,
    ],
]: ...
