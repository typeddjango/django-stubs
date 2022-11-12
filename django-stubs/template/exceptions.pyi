from typing import List, Tuple

from django.template.backends.base import BaseEngine
from django.template.base import Origin

class TemplateDoesNotExist(Exception):
    backend: BaseEngine | None = ...
    tried: List[Tuple[Origin, str]] = ...
    chain: List[TemplateDoesNotExist] = ...
    def __init__(
        self,
        msg: Origin | str,
        tried: List[Tuple[Origin, str]] | None = ...,
        backend: BaseEngine | None = ...,
        chain: List[TemplateDoesNotExist] | None = ...,
    ) -> None: ...

class TemplateSyntaxError(Exception): ...
