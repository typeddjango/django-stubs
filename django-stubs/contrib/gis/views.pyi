from typing import Dict, Type

from django.contrib.gis.feeds import Feed
from django.http import HttpRequest, HttpResponse

def feed(request: HttpRequest, url: str, feed_dict: Dict[str, Type[Feed]] | None = ...) -> HttpResponse: ...
