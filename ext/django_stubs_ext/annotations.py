from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Any, Generic

from django.db.models.base import Model
from typing_extensions import TypeAliasType, TypeVar

# Really, we would like to use TypedDict as a bound, but it's not possible
_Annotations_co = TypeVar("_Annotations_co", covariant=True, bound=Mapping[str, Any])


class Annotations(Generic[_Annotations_co]):
    """Use as `Annotations[MyTypedDict]`"""


_T = TypeVar("_T", bound=Model)

# TODO: 3.12+: `type WithAnnotations[_T: Model, _Annotations_co: Mapping[str, Any]] = Annotated[...]`
WithAnnotations = TypeAliasType(
    "WithAnnotations", Annotated[_T, Annotations[_Annotations_co]], type_params=(_T, _Annotations_co)
)
"""Alias to make it easy to annotate the model `_T` as having annotations
`_Annotations_co` (a `TypedDict`).

Use as `WithAnnotations[MyModel, MyTypedDict]`.
"""
