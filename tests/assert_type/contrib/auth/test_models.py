from __future__ import annotations

from typing import assert_type

from django.contrib.auth.models import AbstractBaseUser, User, UserManager


class MyUser(AbstractBaseUser):
    pass


class Manager(UserManager[MyUser]):
    pass


assert_type(Manager().create_user("username"), MyUser)

assert_type(User.objects, UserManager[User])
assert_type(User.objects.create_superuser("admin"), User)
