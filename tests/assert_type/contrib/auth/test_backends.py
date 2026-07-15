from __future__ import annotations

from typing import Any

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from typing_extensions import assert_type


# Regression test for https://github.com/typeddjango/django-stubs/issues/2591
# ModelBackend.authenticate is relaxed to match BaseBackend
# (self, request, **kwargs), so subclasses can accept custom credentials
# without an [override] error.
class CodeBackend(ModelBackend):
    def authenticate(self, request: object = None, code: str | None = None, **kwargs: Any) -> User | None:
        return User.objects.filter(username=code).first()


class TokenBackend(ModelBackend):
    async def aauthenticate(self, request: object = None, token: str = "", **kwargs: Any) -> User | None:
        return User.objects.filter(username=token).first()


# The base ModelBackend contract still accepts keyword credentials.
ModelBackend().authenticate(request=None, username="u", password="p")
assert_type(
    CodeBackend().authenticate(request=None, code="abc"),
    User | None,
)
