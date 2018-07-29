from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from typing import (
    Callable,
    List,
)


class AccessMixin:
    def get_permission_denied_message(self) -> str: ...
    def get_redirect_field_name(self) -> str: ...
    def handle_no_permission(self): ...


class LoginRequiredMixin:
    def dispatch(self, request: WSGIRequest, *args, **kwargs): ...


class PermissionRequiredMixin:
    def dispatch(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponse: ...
    def get_permission_required(self) -> List[str]: ...


class UserPassesTestMixin:
    def get_test_func(self) -> Callable: ...