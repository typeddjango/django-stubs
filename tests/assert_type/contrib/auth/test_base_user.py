from __future__ import annotations

from django.contrib.auth.models import User
from typing_extensions import assert_type


def get_backend() -> str:
    return "django.contrib.auth.backends.ModelBackend"


user = User()
user.backend = get_backend()
assert_type(user.backend, str)
