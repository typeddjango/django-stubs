from io import (
    BufferedReader,
    TextIOWrapper,
)
from django.core.serializers.base import DeserializedObject
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
)
from typing import (
    List,
    Optional,
    Type,
    Union,
)
from xml.dom.minidom import Element


def getInnerText(node: Element) -> str: ...


class DefusedExpatParser:
    def __init__(self, *args, **kwargs) -> None: ...
    def reset(self) -> None: ...


class Deserializer:
    def __init__(
        self,
        stream_or_string: Union[str, TextIOWrapper, BufferedReader],
        *,
        using = ...,
        ignorenonexistent = ...,
        **options
    ) -> None: ...
    def __next__(self) -> DeserializedObject: ...
    def _get_model_from_node(self, node: Element, attr: str) -> Type[Model]: ...
    def _handle_fk_field_node(
        self,
        node: Element,
        field: ForeignKey
    ) -> Optional[int]: ...
    def _handle_m2m_field_node(
        self,
        node: Element,
        field: ManyToManyField
    ) -> List[int]: ...
    def _handle_object(self, node: Element) -> DeserializedObject: ...
    def _make_parser(self) -> DefusedExpatParser: ...


class Serializer:
    def _start_relational_field(
        self,
        field: Union[ManyToManyField, ForeignKey]
    ) -> None: ...
    def end_object(self, obj: Model) -> None: ...
    def end_serialization(self) -> None: ...
    def handle_field(self, obj: Model, field: Field) -> None: ...
    def handle_fk_field(
        self,
        obj: Model,
        field: ForeignKey
    ) -> None: ...
    def handle_m2m_field(
        self,
        obj: Model,
        field: ManyToManyField
    ) -> None: ...
    def indent(self, level: int) -> None: ...
    def start_object(self, obj: Model) -> None: ...
    def start_serialization(self) -> None: ...