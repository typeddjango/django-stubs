from django.forms import JSONField as BuiltinJSONField
from typing import Any

class JSONField(BuiltinJSONField):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
