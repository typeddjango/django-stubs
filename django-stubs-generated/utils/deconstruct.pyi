from typing import Any, Optional, Type, Union

from django.contrib.postgres.validators import KeysValidator
from django.core.validators import RegexValidator


def deconstructible(
    *args: Any, path: Optional[Any] = ...
) -> Type[Union[KeysValidator, RegexValidator]]: ...
