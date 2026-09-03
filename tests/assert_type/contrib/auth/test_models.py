from __future__ import annotations

from typing import assert_type

from django.contrib.auth.models import AbstractBaseUser, UserManager
from typing_extensions import override


class MyUser(AbstractBaseUser):
    @override
    def natural_key(self) -> tuple[str, str]:
        return (self.get_username(), self.password)


class Manager(UserManager[MyUser]):
    pass


class MyOtherUser(AbstractBaseUser):
    @override
    def natural_key(self) -> tuple[()]:
        return ()


class NonUniqueManager(UserManager[MyOtherUser]):
    pass


assert_type(Manager().create_user("username"), MyUser)
assert_type(NonUniqueManager().create_user("username"), MyOtherUser)
