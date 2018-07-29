from io import (
    BufferedReader,
    StringIO,
    TextIOWrapper,
)
from collections import OrderedDict
from django.core.exceptions import ValidationError
from django.core.serializers.xml_serializer import Deserializer
from django.db.models.base import Model
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
)
from django.db.models.query import QuerySet
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)
from uuid import UUID


def build_instance(
    Model: Type[Model],
    data: Dict[str, Any],
    db: str
) -> Model: ...


def deserialize_fk_value(
    field: ForeignKey,
    field_value: Any,
    using: str
) -> Optional[Union[str, UUID, int]]: ...


def deserialize_m2m_values(
    field: ManyToManyField,
    field_value: Union[List[List[str]], List[int], List[Union[int, str]]],
    using: str
) -> List[int]: ...


class DeserializationError:
    @classmethod
    def WithData(
        cls,
        original_exc: ValidationError,
        model: str,
        fk: str,
        field_value: None
    ) -> DeserializationError: ...


class DeserializedObject:
    def __init__(self, obj: Model, m2m_data: Dict[str, List[int]] = ...) -> None: ...
    def __repr__(self) -> str: ...
    def save(self, save_m2m: bool = ..., using: Optional[str] = ..., **kwargs) -> None: ...


class Deserializer:
    def __init__(self, stream_or_string: Union[str, TextIOWrapper, BufferedReader], **options) -> None: ...
    def __iter__(self) -> Deserializer: ...


class M2MDeserializationError:
    def __init__(self, original_exc: ValidationError, pk: str) -> None: ...


class ProgressBar:
    def __init__(self, output: Optional[StringIO], total_count: int) -> None: ...
    def update(self, count: int) -> None: ...


class Serializer:
    def getvalue(self) -> Optional[str]: ...
    def serialize(
        self,
        queryset: Union[List[Model], QuerySet],
        *,
        stream = ...,
        fields = ...,
        use_natural_foreign_keys = ...,
        use_natural_primary_keys = ...,
        progress_output = ...,
        object_count = ...,
        **options
    ) -> Optional[Union[str, List[OrderedDict]]]: ...