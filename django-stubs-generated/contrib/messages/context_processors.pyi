from typing import Any, Dict, List, Optional, Union

from django.contrib.messages.storage.base import BaseStorage
from django.http.request import HttpRequest

def messages(request: HttpRequest) -> Dict[str, Union[Dict[str, int], List[Any], BaseStorage]]: ...
