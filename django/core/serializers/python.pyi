from collections import OrderedDict
from django.core.serializers.base import DeserializedObject
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
)
from typing import (
    Any,
    Iterator,
    List,
)


def Deserializer(
    object_list: Any,
    *,
    using = ...,
    ignorenonexistent = ...,
    **options
) -> Iterator[DeserializedObject]: ...


def _get_model(model_identifier: str) -> Any: ...


class Serializer:
    def _value_from_field(self, obj: Model, field: Field) -> Any: ...
    def end_object(self, obj: Model) -> None: ...
    def end_serialization(self) -> None: ...
    def get_dump_object(self, obj: Model) -> OrderedDict: ...
    def getvalue(self) -> List[OrderedDict]: ...
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
    def start_object(self, obj: Model) -> None: ...
    def start_serialization(self) -> None: ...