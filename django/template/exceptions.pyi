from django.template.backends.base import BaseEngine
from django.template.base import Origin
from typing import (
    List,
    Optional,
    Tuple,
    Union,
)


class TemplateDoesNotExist:
    def __init__(
        self,
        msg: Union[str, Origin],
        tried: Optional[List[Tuple[Origin, str]]] = ...,
        backend: Optional[BaseEngine] = ...,
        chain: Optional[List[TemplateDoesNotExist]] = ...
    ) -> None: ...