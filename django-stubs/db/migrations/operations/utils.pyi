import sys
from collections import namedtuple
from typing import Iterator, Optional, Tuple, Union

from django.db.migrations.state import ModelState, ProjectState
from django.db.models import Field

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

def resolve_relation(model, app_label: Optional[str] = ..., model_name: Optional[str] = ...) -> Tuple[str, str]: ...

FieldReference = namedtuple("FieldReference", ["to", "through"])

def field_references(
    model_tuple: Tuple[str, str],
    field: Field,
    reference_model_tuple: Tuple[str, str],
    reference_field_name: Optional[str] = ...,
    reference_field: Optional[Field] = ...,
) -> Union[Literal[False], FieldReference]: ...
def get_references(
    state: ProjectState,
    model_tuple: Tuple[str, str],
    field_tuple: Union[Tuple[()], Tuple[str, Field]] = ...,
) -> Iterator[Tuple[ModelState, str, Field, FieldReference]]: ...
def field_is_referenced(state: ProjectState, model_tuple: Tuple[str, str], field_tuple: Tuple[str, Field]) -> bool: ...
