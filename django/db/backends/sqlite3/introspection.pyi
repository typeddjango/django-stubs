from django.db.backends.base.introspection import (
    FieldInfo,
    TableInfo,
)
from django.db.backends.utils import CursorWrapper
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def get_field_size(name: str) -> Optional[int]: ...


class DatabaseIntrospection:
    def _get_foreign_key_constraints(
        self,
        cursor: CursorWrapper,
        table_name: str
    ) -> Dict[str, Dict[str, Union[List[str], bool, Tuple[str, str]]]]: ...
    def _table_info(
        self,
        cursor: CursorWrapper,
        name: str
    ) -> List[Dict[str, Union[str, None, int]]]: ...
    def get_constraints(
        self,
        cursor: CursorWrapper,
        table_name: str
    ) -> Dict[str, Dict[str, Union[List[str], bool, str, Tuple[str, str]]]]: ...
    def get_key_columns(
        self,
        cursor: CursorWrapper,
        table_name: str
    ) -> List[Tuple[str, str, str]]: ...
    def get_primary_key_column(self, cursor: CursorWrapper, table_name: str) -> str: ...
    def get_relations(
        self,
        cursor: CursorWrapper,
        table_name: str
    ) -> Dict[str, Tuple[str, str]]: ...
    def get_sequences(
        self,
        cursor: CursorWrapper,
        table_name: str,
        table_fields: List[Union[ForeignKey, CharField]] = ...
    ) -> List[Dict[str, str]]: ...
    def get_table_description(
        self,
        cursor: CursorWrapper,
        table_name: str
    ) -> List[FieldInfo]: ...
    def get_table_list(
        self,
        cursor: CursorWrapper
    ) -> List[TableInfo]: ...


class FlexibleFieldLookupDict:
    def __getitem__(self, key: str) -> Union[str, Tuple[str, Dict[str, int]]]: ...