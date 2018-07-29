from collections import OrderedDict
from django.apps.config import AppConfig
from django.contrib.admin.apps import SimpleAdminConfig
from django.contrib.sites.apps import SitesConfig
from django.core.serializers.json import Serializer
from django.core.serializers.python import Serializer
from django.core.serializers.xml_serializer import (
    Deserializer,
    Serializer,
)
from django.db.models.base import Model
from django.db.models.query import QuerySet
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


def _load_serializers() -> None: ...


def deserialize(format: str, stream_or_string: Any, **options) -> Deserializer: ...


def get_deserializer(format: str) -> Union[Type[Deserializer], Callable]: ...


def get_public_serializer_formats() -> List[str]: ...


def get_serializer(
    format: str
) -> Union[Type[Serializer], Type[Serializer], Type[Serializer], BadSerializer]: ...


def register_serializer(format: str, serializer_module: str, serializers: Dict[str, Any] = ...) -> None: ...


def serialize(
    format: str,
    queryset: Union[List[Model], QuerySet],
    **options
) -> Optional[Union[str, List[OrderedDict]]]: ...


def sort_dependencies(
    app_list: Union[List[Union[Tuple[SitesConfig, None], Tuple[SimpleAdminConfig, None], Tuple[AppConfig, None]]], List[Tuple[str, List[Type[Model]]]], List[Union[Tuple[SitesConfig, None], Tuple[SimpleAdminConfig, None]]]]
) -> List[Type[Model]]: ...


class BadSerializer:
    def __call__(self, *args, **kwargs): ...
    def __init__(self, exception: ModuleNotFoundError) -> None: ...