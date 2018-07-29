from collections import OrderedDict
from django.core.management.base import CommandParser
from django.db.backends.base.introspection import FieldInfo
from django.db.backends.sqlite3.base import DatabaseWrapper
from typing import Any, Dict, Iterator, List, Tuple, Union

class Command:
    def add_arguments(self, parser: CommandParser) -> None: ...
    def get_field_type(
        self, connection: DatabaseWrapper, table_name: str, row: FieldInfo
    ) -> Union[Tuple[str, OrderedDict, List[Any]], Tuple[str, OrderedDict, List[str]]]: ...
    def get_meta(
        self,
        table_name: str,
        constraints: Dict[str, Dict[str, Union[List[str], bool, str, Tuple[str, str]]]],
        column_to_field_name: Dict[str, str],
        is_view: bool,
    ) -> List[str]: ...
    def handle(self, **options) -> None: ...
    def handle_inspection(self, options: Dict[str, Any]) -> Iterator[str]: ...
    def normalize_col_name(
        self, col_name: str, used_column_names: List[str], is_relation: bool
    ) -> Union[
        Tuple[str, Dict[Any, Any], List[Any]], Tuple[str, Dict[str, str], List[str]]
    ]: ...
