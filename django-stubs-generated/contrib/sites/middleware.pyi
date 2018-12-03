from typing import Any, Optional

from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from .shortcuts import get_current_site

class CurrentSiteMiddleware(MiddlewareMixin):
    get_response: None
    def process_request(self, request: HttpRequest) -> None: ...
