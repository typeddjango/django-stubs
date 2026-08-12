from __future__ import annotations

from typing import assert_type

from django.contrib.auth.models import User


def get_backend() -> str:
    return "django.contrib.auth.backends.ModelBackend"


user = User()
user.backend = get_backend()
assert_type(user.backend, str)
