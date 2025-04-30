from django.contrib.auth.models import AbstractBaseUser, UserManager
from typing_extensions import assert_type


class MyUser(AbstractBaseUser):
    pass


class Manager(UserManager[MyUser]):
    pass


assert_type(Manager().create_user("username"), MyUser)
