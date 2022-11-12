from typing import Any, Dict, List

from django.contrib.messages.storage.base import BaseStorage
from django.http.request import HttpRequest

def messages(request: HttpRequest) -> Dict[str, Dict[str, int] | List[Any] | BaseStorage]: ...
