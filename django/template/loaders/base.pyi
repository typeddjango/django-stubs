from django.template.base import (
    Origin,
    Template,
)
from django.template.engine import Engine
from typing import (
    List,
    Optional,
)


class Loader:
    def __init__(self, engine: Engine) -> None: ...
    def get_template(
        self,
        template_name: str,
        skip: Optional[List[Origin]] = ...
    ) -> Template: ...