from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorWrapper
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class BaseDatabaseIntrospection:
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...
    def column_name_converter(self, name: str) -> str: ...
    def django_table_names(self, only_existing: bool = ..., include_views: bool = ...) -> List[str]: ...
    def get_field_type(
        self,
        data_type: str,
        description: FieldInfo
    ) -> Union[str, Tuple[str, Dict[str, int]]]: ...
    def table_name_converter(self, name: str) -> str: ...
    def table_names(
        self,
        cursor: Optional[CursorWrapper] = ...,
        include_views: bool = ...
    ) -> List[str]: ...