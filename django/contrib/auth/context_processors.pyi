from auth_tests.test_context_processors import MockUser
from django.contrib.auth.models import (
    AnonymousUser,
    User,
)
from django.http.request import HttpRequest
from typing import (
    Dict,
    Union,
)


def auth(
    request: HttpRequest
) -> Dict[str, Union[AnonymousUser, PermWrapper, User]]: ...


class PermLookupDict:
    def __bool__(self) -> bool: ...
    def __getitem__(self, perm_name: str) -> bool: ...
    def __init__(self, user: MockUser, app_label: str) -> None: ...


class PermWrapper:
    def __contains__(self, perm_name: str) -> bool: ...
    def __getitem__(self, app_label: str) -> PermLookupDict: ...
    def __init__(
        self,
        user: Union[MockUser, AnonymousUser, User]
    ) -> None: ...
    def __iter__(self): ...