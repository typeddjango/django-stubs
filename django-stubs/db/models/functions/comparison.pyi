from typing import Any, Union

from django.db.models import Func
from django.db.models.fields import Field
from django.db.models.fields.json import JSONField

class Cast(Func):
    def __init__(self, expression: Any, output_field: Union[str, Field]) -> None: ...

class Coalesce(Func): ...
class Greatest(Func): ...

class JSONObject(Func):
    output_field: JSONField

class Least(Func): ...
class NullIf(Func): ...
