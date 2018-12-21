from typing import Any, List, Optional

from django.core.checks.messages import Error
from django.db.models.query import QuerySet

from django.db import models

class CurrentSiteManager(models.Manager):
    creation_counter: int
    model: None
    name: None
    use_in_migrations: bool = ...
    def __init__(self, field_name: Optional[str] = ...) -> None: ...
    def check(self, **kwargs: Any) -> List[Error]: ...
    def get_queryset(self) -> QuerySet: ...
