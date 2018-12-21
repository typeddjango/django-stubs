from typing import Any, List, Optional, Tuple, Union

from django.template.backends.base import BaseEngine
from django.template.base import Origin

class TemplateDoesNotExist(Exception):
    backend: Optional[django.template.backends.base.BaseEngine] = ...
    tried: List[Tuple[django.template.base.Origin, str]] = ...
    chain: List[django.template.exceptions.TemplateDoesNotExist] = ...
    def __init__(
        self,
        msg: Union[Origin, str],
        tried: Optional[List[Tuple[Origin, str]]] = ...,
        backend: Optional[BaseEngine] = ...,
        chain: Optional[List[TemplateDoesNotExist]] = ...,
    ) -> None: ...

class TemplateSyntaxError(Exception): ...
