from typing import Any, Optional, Type, Union

from django.contrib.auth.validators import (ASCIIUsernameValidator,
                                            UnicodeUsernameValidator)
from django.contrib.postgres.validators import KeysValidator


def deconstructible(
    *args: Any, path: Optional[Any] = ...
) -> Type[
    Union[ASCIIUsernameValidator, UnicodeUsernameValidator, KeysValidator]
]: ...
