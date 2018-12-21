from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

class CurrentSiteMiddleware(MiddlewareMixin):
    get_response: None
    def process_request(self, request: HttpRequest) -> None: ...
