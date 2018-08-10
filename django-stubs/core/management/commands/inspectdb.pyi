from collections import OrderedDict
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from django.core.management.base import BaseCommand, CommandParser
from django.db.backends.base.introspection import FieldInfo
from django.db.backends.sqlite3.base import DatabaseWrapper


class Command(BaseCommand):
    stderr: django.core.management.base.OutputWrapper
    stdout: django.core.management.base.OutputWrapper
    style: django.core.management.color.Style
    help: str = ...
    requires_system_checks: bool = ...
    stealth_options: Any = ...
    db_module: str = ...
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, **options: Any) -> None: ...
    def handle_inspection(self, options: Dict[str, Any]) -> Iterator[str]: ...
    def normalize_col_name(
        self, col_name: str, used_column_names: List[str], is_relation: bool
    ) -> Tuple[str, Dict[str, str], List[str]]: ...
    def get_field_type(
        self, connection: DatabaseWrapper, table_name: str, row: FieldInfo
    ) -> Tuple[str, OrderedDict, List[str]]: ...
    def get_meta(
        self,
        table_name: str,
        constraints: Dict[
            str,
            Union[
                Dict[str, Union[List[str], Tuple[str, str], bool]],
                Dict[str, Union[List[str], bool, str]],
            ],
        ],
        column_to_field_name: Dict[str, str],
        is_view: bool,
    ) -> List[str]: ...
