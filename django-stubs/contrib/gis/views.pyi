from typing import Dict, Optional, Type

from django.contrib.gis.feeds import Feed
from django.http import HttpRequest, HttpResponse

def feed(request: HttpRequest, url: str, feed_dict: Optional[Dict[str, Type[Feed]]] = ...) -> HttpResponse: ...
