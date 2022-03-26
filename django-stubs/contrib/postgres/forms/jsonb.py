from typing import Any

from django.forms import JSONField as BuiltinJSONField


# Deprecated, removed in 4.0
class JSONField(BuiltinJSONField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...
