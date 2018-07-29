from django.db.migrations.migration import Migration
from typing import (
    Optional,
    Tuple,
    Union,
)


class NodeNotFoundError:
    def __init__(
        self,
        message: str,
        node: Tuple[str, str],
        origin: Optional[Union[str, Migration]] = ...
    ) -> None: ...
    def __str__(self) -> str: ...