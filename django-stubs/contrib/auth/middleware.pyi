from collections.abc import Callable
from typing import Any, ClassVar

from django.contrib.auth.models import _AnyUser
from django.http import HttpRequest, HttpResponseBase, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

def get_user(request: HttpRequest) -> _AnyUser: ...
async def auser(request: HttpRequest) -> _AnyUser: ...

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None: ...

class LoginRequiredMiddleware(MiddlewareMixin):
    redirect_field_name: ClassVar[str]

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponseBase],
        view_args: tuple[Any, ...],
        view_kwargs: dict[Any, Any],
    ) -> HttpResponseBase | None: ...
    def get_login_url(self, view_func: Callable[..., HttpResponseBase]) -> str: ...
    def get_redirect_field_name(self, view_func: Callable[..., HttpResponseBase]) -> str: ...
    def handle_no_permission(
        self, request: HttpRequest, view_func: Callable[..., HttpResponseBase]
    ) -> HttpResponseRedirect: ...

class RemoteUserMiddleware(MiddlewareMixin):
    header: str
    force_logout_if_no_header: bool
    def clean_username(self, username: str, request: HttpRequest) -> str: ...

class PersistentRemoteUserMiddleware(RemoteUserMiddleware):
    force_logout_if_no_header: bool
