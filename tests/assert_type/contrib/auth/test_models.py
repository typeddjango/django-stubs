from __future__ import annotations

from typing import assert_type

from django.contrib.auth.models import AbstractBaseUser, UserManager


class MyUser(AbstractBaseUser):
    pass


class Manager(UserManager[MyUser]):
    pass


assert_type(Manager().create_user("username"), MyUser)
