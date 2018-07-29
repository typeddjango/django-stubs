from django.contrib.postgres.validators import KeysValidator
from django.core.validators import RegexValidator
from typing import (
    Type,
    Union,
)


def deconstructible(
    *args,
    path = ...
) -> Type[Union[KeysValidator, RegexValidator]]: ...