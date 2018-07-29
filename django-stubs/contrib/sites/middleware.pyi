from django.http.request import HttpRequest


class CurrentSiteMiddleware:
    def process_request(self, request: HttpRequest) -> None: ...