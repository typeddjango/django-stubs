from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

_UserModel = get_user_model()

def get_user(request: HttpRequest) -> AnonymousUser | _UserModel: ...

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None: ...

class RemoteUserMiddleware(MiddlewareMixin):
    header: str
    force_logout_if_no_header: bool
    def process_request(self, request: HttpRequest) -> None: ...
    def clean_username(self, username: str, request: HttpRequest) -> str: ...

class PersistentRemoteUserMiddleware(RemoteUserMiddleware):
    force_logout_if_no_header: bool
