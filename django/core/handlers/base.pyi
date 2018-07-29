from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    FileResponse,
    HttpResponse,
    HttpResponseBase,
)
from typing import (
    Callable,
    Union,
)


class BaseHandler:
    def _get_response(
        self,
        request: WSGIRequest
    ) -> Union[HttpResponse, FileResponse]: ...
    def get_response(self, request: WSGIRequest) -> HttpResponseBase: ...
    def load_middleware(self) -> None: ...
    def make_view_atomic(self, view: Callable) -> Callable: ...
    def process_exception_by_middleware(
        self,
        exception: Exception,
        request: WSGIRequest
    ) -> HttpResponse: ...