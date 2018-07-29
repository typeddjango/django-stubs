from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
    Union,
)


def serializer_factory(value: Any) -> BaseSerializer: ...


class BaseSequenceSerializer:
    def serialize(self) -> Union[Tuple[str, Set[str]], Tuple[str, Set[Any]]]: ...


class BaseSerializer:
    def __init__(self, value: Any) -> None: ...


class BaseSimpleSerializer:
    def serialize(self) -> Tuple[str, Set[Any]]: ...


class DateSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class DatetimeSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class DeconstructableSerializer:
    @staticmethod
    def _serialize_path(path: str) -> Tuple[str, Set[str]]: ...
    def serialize(self) -> Tuple[str, Set[str]]: ...
    @staticmethod
    def serialize_deconstructed(
        path: str,
        args: Union[List[str], Tuple],
        kwargs: Dict[str, object]
    ) -> Tuple[str, Set[str]]: ...


class DictionarySerializer:
    def serialize(self) -> Tuple[str, Set[Any]]: ...


class EnumSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class FloatSerializer:
    def serialize(self) -> Tuple[str, Set[Any]]: ...


class FrozensetSerializer:
    def _format(self) -> str: ...


class FunctionTypeSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class ModelFieldSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class ModelManagerSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class OperationSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class RegexSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class SequenceSerializer:
    def _format(self) -> str: ...


class SetSerializer:
    def _format(self) -> str: ...


class TimedeltaSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...


class TupleSerializer:
    def _format(self) -> str: ...


class TypeSerializer:
    def serialize(self) -> Union[Tuple[str, Set[str]], Tuple[str, Set[Any]]]: ...


class UUIDSerializer:
    def serialize(self) -> Tuple[str, Set[str]]: ...