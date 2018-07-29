from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.base import Model
from django.db.models.fields import (
    DateTimeCheckMixin,
    Field,
)
from django.utils.datastructures import ImmutableList
from typing import (
    Any,
    Dict,
    Optional,
    Set,
    Type,
    Union,
)


class Options:
    def __init__(self, meta: Any, app_label: str = ...) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def _expire_cache(self, forward: bool = ..., reverse: bool = ...) -> None: ...
    @cached_property
    def _forward_fields_map(
        self
    ) -> Dict[str, Union[GenericForeignKey, Field, DateTimeCheckMixin]]: ...
    def _get_fields(
        self,
        forward: bool = ...,
        reverse: bool = ...,
        include_parents: object = ...,
        include_hidden: bool = ...,
        seen_models: Optional[Set[Type[Model]]] = ...
    ) -> ImmutableList: ...
    def _populate_directed_relation_graph(self) -> Any: ...
    def _prepare(self, model: Type[Model]) -> None: ...