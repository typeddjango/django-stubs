from datetime import date, datetime
from itertools import chain
from typing import (Any, Callable, Dict, Iterator, List, Optional, Sequence,
                    Set, Tuple, Type, Union)

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.utils import CursorWrapper
from django.db.models.base import Model
from django.db.models.expressions import (Col, Expression, OrderBy,
                                          SQLiteNumericMixin)
from django.db.models.fields import Field
from django.db.models.fields.files import ImageFieldFile
from django.db.models.fields.related import ForeignKey, ForeignObject
from django.db.models.options import Options
from django.db.models.sql.query import Query
from django.utils.datastructures import ImmutableList

FORCE: Any

class SQLCompiler:
    query: Any = ...
    connection: Any = ...
    using: Any = ...
    quote_cache: Any = ...
    select: Any = ...
    annotation_col_map: Any = ...
    klass_info: Any = ...
    ordering_parts: Any = ...
    def __init__(
        self, query: Query, connection: DatabaseWrapper, using: str
    ) -> None: ...
    col_count: Any = ...
    def setup_query(self) -> None: ...
    has_extra_select: Any = ...
    def pre_sql_setup(
        self
    ) -> Tuple[
        List[Any], List[Tuple[OrderBy, Tuple[str, List[int], bool]]], List[Any]
    ]: ...
    def get_group_by(
        self,
        select: List[Tuple[Expression, Tuple[str, List[int]], Optional[str]]],
        order_by: List[Tuple[OrderBy, Tuple[str, List[int], bool]]],
    ) -> List[Tuple[str, List[Any]]]: ...
    def collapse_group_by(
        self, expressions: List[Expression], having: Tuple
    ) -> List[Expression]: ...
    def get_select(
        self
    ) -> Union[
        Tuple[
            List[Tuple[Expression, Tuple[str, List[Any]], Union[None, str]]],
            Dict[
                str,
                Union[
                    Type[Model],
                    List[int],
                    List[
                        Dict[
                            str,
                            Union[
                                Type[User],
                                ForeignKey,
                                bool,
                                Callable,
                                List[int],
                            ],
                        ]
                    ],
                ],
            ],
            Union[Dict[Any, Any], Dict[str, int]],
            Dict[str, int],
        ],
        Tuple[
            List[Tuple[Expression, Tuple[str, List[Any]], str]],
            None,
            Dict[str, int],
        ],
        Tuple[
            List[Tuple[Col, Tuple[str, List[Any]], None]],
            Dict[
                str,
                Union[
                    Type[LogEntry],
                    List[int],
                    List[
                        Dict[
                            str,
                            Union[
                                Type[User],
                                ForeignKey,
                                bool,
                                Callable,
                                List[int],
                            ],
                        ]
                    ],
                ],
            ],
            Dict[Any, Any],
        ],
    ]: ...
    def get_order_by(
        self
    ) -> List[Tuple[OrderBy, Tuple[str, List[int], bool]]]: ...
    def get_extra_select(
        self,
        order_by: List[Tuple[OrderBy, Tuple[str, List[int], bool]]],
        select: List[Tuple[Expression, Tuple[str, List[int]], Optional[str]]],
    ) -> List[Any]: ...
    def quote_name_unless_alias(self, name: str) -> str: ...
    def compile(
        self, node: Any, select_format: bool = ...
    ) -> Tuple[str, Sequence]: ...
    def get_combinator_sql(self, combinator: Any, all: Any): ...
    def as_sql(
        self, with_limits: bool = ..., with_col_aliases: bool = ...
    ) -> Any: ...
    def get_default_columns(
        self, start_alias: None = ..., opts: None = ..., from_parent: None = ...
    ) -> List[Col]: ...
    def get_distinct(self) -> Tuple[List[Any], List[Any]]: ...
    def find_ordering_name(
        self,
        name: str,
        opts: Options,
        alias: None = ...,
        default_order: str = ...,
        already_seen: None = ...,
    ) -> List[Tuple[OrderBy, bool]]: ...
    def get_from_clause(self) -> Tuple[List[str], List[Any]]: ...
    def get_related_selections(
        self,
        select: List[Tuple[Col, None]],
        opts: Optional[Options] = ...,
        root_alias: Optional[str] = ...,
        cur_depth: int = ...,
        requested: Optional[bool] = ...,
        restricted: Optional[bool] = ...,
    ) -> Union[
        List[
            Dict[
                str,
                Union[Type[Model], ForeignObject, bool, Callable, List[int]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[Type[User], ForeignKey, bool, Callable, List[int]],
                ],
                Dict[
                    str,
                    Union[
                        Type[ContentType], ForeignKey, bool, Callable, List[int]
                    ],
                ],
            ]
        ],
        List[
            Dict[str, Union[Type[Group], ForeignKey, bool, Callable, List[int]]]
        ],
    ]: ...
    def get_select_for_update_of_arguments(self): ...
    def deferred_to_columns(self) -> Dict[Type[Model], Set[str]]: ...
    def get_converters(
        self, expressions: List[Expression]
    ) -> Dict[int, Tuple[List[Callable], Expression]]: ...
    def apply_converters(
        self,
        rows: chain,
        converters: Dict[
            int,
            Union[
                Tuple[List[Callable], SQLiteNumericMixin],
                Tuple[List[Callable], Col],
            ],
        ],
    ) -> Iterator[List[Optional[Union[int, date, str]]]]: ...
    def results_iter(
        self,
        results: Any = ...,
        tuple_expected: bool = ...,
        chunked_fetch: bool = ...,
        chunk_size: int = ...,
    ) -> Union[Iterator[Any], chain]: ...
    def has_results(self) -> bool: ...
    def execute_sql(
        self,
        result_type: str = ...,
        chunked_fetch: bool = ...,
        chunk_size: int = ...,
    ) -> Union[CursorWrapper, Iterator[Any]]: ...
    def as_subquery_condition(
        self, alias: str, columns: List[str], compiler: SQLCompiler
    ) -> Tuple[str, Tuple]: ...
    def explain_query(self) -> None: ...

class SQLInsertCompiler(SQLCompiler):
    return_id: bool = ...
    def field_as_sql(
        self, field: Field, val: Union[str, float]
    ) -> Tuple[str, Union[List[float], List[str], List[int]]]: ...
    def prepare_value(
        self,
        field: Field,
        value: Union[files.ImageFieldFile, float, str, datetime],
    ) -> Optional[Union[str, float]]: ...
    def pre_save_val(
        self, field: Field, obj: Model
    ) -> Optional[Union[files.ImageFieldFile, float, str, date]]: ...
    def assemble_as_sql(
        self,
        fields: Union[List[Field], ImmutableList],
        value_rows: Union[
            List[List[Union[int, str, None]]], List[List[Union[float, str]]]
        ],
    ) -> Tuple[Tuple[Tuple[str]], List]: ...
    def as_sql(self) -> List: ...
    def execute_sql(self, return_id: bool = ...) -> Any: ...

class SQLDeleteCompiler(SQLCompiler):
    def as_sql(self): ...

class SQLUpdateCompiler(SQLCompiler):
    def as_sql(self) -> Tuple[str, Tuple]: ...
    def execute_sql(self, result_type: str) -> int: ...
    def pre_sql_setup(self) -> None: ...

class SQLAggregateCompiler(SQLCompiler):
    col_count: Any = ...
    def as_sql(self): ...

def cursor_iter(
    cursor: CursorWrapper, sentinel: List[Any], col_count: None, itersize: int
) -> Iterator[List]: ...
