from typing import Optional, TypeVar

from django.contrib.sites.models import Site
from django.db import models

_T = TypeVar("_T", bound=Site)

class CurrentSiteManager(models.Manager[_T]):
    def __init__(self, field_name: Optional[str] = ...) -> None: ...
