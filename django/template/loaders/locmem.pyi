from django.template.base import Origin
from django.template.engine import Engine
from typing import (
    Dict,
    Iterator,
)


class Loader:
    def __init__(self, engine: Engine, templates_dict: Dict[str, str]) -> None: ...
    def get_contents(self, origin: Origin) -> str: ...
    def get_template_sources(self, template_name: str) -> Iterator[Origin]: ...