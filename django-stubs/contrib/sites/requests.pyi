from typing import NoReturn

from django.http.request import HttpRequest

class RequestSite:
    name: str
    domain: str
    def __init__(self, request: HttpRequest) -> None: ...
    def save(self, force_insert: bool = ..., force_update: bool = ...) -> NoReturn: ...
    def delete(self) -> NoReturn: ...
