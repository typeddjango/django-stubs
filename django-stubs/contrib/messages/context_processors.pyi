from django.contrib.messages.storage.base import BaseStorage
from django.http.request import HttpRequest
from typing import (
    Dict,
    Union,
)


def messages(
    request: HttpRequest
) -> Dict[str, Union[Dict[str, int], BaseStorage]]: ...