from typing import Any, Type, TypeVar

from django.db.models.base import Model
from typing_extensions import Annotated


class Annotations:
    def __init__(self, **kwargs: Type[Any]):
        pass


_T = TypeVar("_T", bound=Model)

WithAnnotations = Annotated[_T, Annotations()]
