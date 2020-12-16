from typing import Any, Callable, Optional, Type

from django.contrib.admin.sites import AdminSite
from django.db.models.base import Model

def register(*models: Type[Model], site: Optional[AdminSite] = ...) -> Callable: ...
