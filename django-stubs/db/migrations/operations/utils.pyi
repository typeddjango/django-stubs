from collections import namedtuple
from typing import Iterator, Tuple, Type

from django.db.migrations.state import ModelState, ProjectState
from django.db.models import Field, Model
from typing_extensions import Literal

def resolve_relation(
    model: str | Type[Model], app_label: str | None = ..., model_name: str | None = ...
) -> Tuple[str, str]: ...

FieldReference = namedtuple("FieldReference", ["to", "through"])

def field_references(
    model_tuple: Tuple[str, str],
    field: Field,
    reference_model_tuple: Tuple[str, str],
    reference_field_name: str | None = ...,
    reference_field: Field | None = ...,
) -> Literal[False] | FieldReference: ...
def get_references(
    state: ProjectState,
    model_tuple: Tuple[str, str],
    field_tuple: Tuple[()] | Tuple[str, Field] = ...,
) -> Iterator[Tuple[ModelState, str, Field, FieldReference]]: ...
def field_is_referenced(state: ProjectState, model_tuple: Tuple[str, str], field_tuple: Tuple[str, Field]) -> bool: ...
