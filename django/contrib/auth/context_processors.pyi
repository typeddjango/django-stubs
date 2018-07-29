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
) -> Dict[str, Union[PermWrapper, AnonymousUser, User]]: ...


class PermLookupDict:
    def __bool__(self) -> bool: ...
    def __getitem__(self, perm_name: str) -> bool: ...
    def __init__(self, user: object, app_label: str) -> None: ...


class PermWrapper:
    def __contains__(self, perm_name: str) -> bool: ...
    def __getitem__(self, app_label: str) -> PermLookupDict: ...
    def __init__(self, user: object) -> None: ...
    def __iter__(self): ...