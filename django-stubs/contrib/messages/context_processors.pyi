from typing import Any, Dict, List, Optional, Union

from django.contrib.messages.storage.base import BaseStorage
from django.http.request import HttpRequest


def messages(
    request: HttpRequest
) -> Union[
    Dict[str, Union[Dict[str, int], List[Any]]],
    Dict[str, Union[Dict[str, int], BaseStorage]],
]: ...
