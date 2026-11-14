from typing import Any

from django.db.models.fields import CharField, EmailField, TextField
from typing_extensions import TypeVar

# __set__ value type
_ST_contra = TypeVar("_ST_contra", contravariant=True, default=Any)
# __get__ return type
_GT_co = TypeVar("_GT_co", covariant=True, default=Any)

class CICharField(CharField[_ST_contra, _GT_co]): ...
class CIEmailField(EmailField[_ST_contra, _GT_co]): ...
class CITextField(TextField[_ST_contra, _GT_co]): ...

__all__ = ["CICharField", "CIEmailField", "CITextField"]
