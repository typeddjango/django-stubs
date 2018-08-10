from datetime import date, datetime, time, timedelta
from decimal import Decimal
from itertools import chain
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Type, Union)
from uuid import UUID

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.utils import CursorWrapper
from django.db.models.base import Model
from django.db.models.expressions import (BaseExpression, Col, Combinable,
                                          Expression, OrderBy, RawSQL,
                                          SQLiteNumericMixin)
from django.db.models.fields import Field
from django.db.models.fields.files import FieldFile
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import (ForeignKey, ForeignObject,
                                             OneToOneField)
from django.db.models.functions.text import Lower
from django.db.models.lookups import Lookup
from django.db.models.options import Options
from django.db.models.query_utils import FilteredRelation, QueryWrapper
from django.db.models.sql.datastructures import BaseTable, Join
from django.db.models.sql.query import Query, RawQuery
from django.db.models.sql.where import (ExtraWhere, NothingNode,
                                        SubqueryConstraint, WhereNode)
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
        self,
        query: Union[Query, RawQuery],
        connection: DatabaseWrapper,
        using: Optional[str],
    ) -> None: ...
    col_count: Any = ...
    def setup_query(self) -> None: ...
    has_extra_select: Any = ...
    def pre_sql_setup(
        self
    ) -> Union[
        Tuple[
            List[Any],
            List[Any],
            List[Union[Tuple[str, List[Any]], Tuple[str, List[str]]]],
        ],
        Tuple[
            List[Any],
            List[
                Tuple[
                    OrderBy,
                    Union[
                        Tuple[str, List[Any], bool],
                        Tuple[str, List[int], bool],
                        Tuple[str, List[str], bool],
                        Tuple[str, Tuple, bool],
                    ],
                ]
            ],
            List[
                Union[Any, Tuple[str, Union[List[Any], List[float], List[int]]]]
            ],
        ],
        Tuple[
            List[Tuple[OrderBy, None, None]],
            List[
                Tuple[
                    OrderBy,
                    Union[
                        Tuple[str, List[Union[int, str]], bool],
                        Tuple[str, Tuple[str, str], bool],
                    ],
                ]
            ],
            List[Union[Any, Tuple[str, List[int]]]],
        ],
    ]: ...
    def get_group_by(
        self,
        select: List[Tuple[BaseExpression, Optional[str], Optional[str]]],
        order_by: List[
            Tuple[
                OrderBy,
                Union[
                    Tuple[str, List[Any], bool],
                    Tuple[str, List[Union[int, str]], bool],
                    Tuple[str, List[int], bool],
                    Tuple[str, List[str], bool],
                    Tuple[str, Tuple, bool],
                    Tuple[str, Tuple[str, str], bool],
                ],
            ]
        ],
    ) -> List[
        Tuple[str, Union[List[Any], List[float], List[int], List[str]]]
    ]: ...
    def collapse_group_by(
        self,
        expressions: List[Expression],
        having: Union[List[Expression], Tuple],
    ) -> List[Expression]: ...
    def get_select(
        self
    ) -> Union[
        Tuple[
            List[Tuple[Col, Tuple[str, List[Any]], None]],
            Dict[
                str,
                Union[
                    List[
                        Dict[
                            str,
                            Union[
                                Callable,
                                List[Any],
                                List[int],
                                Type[Model],
                                bool,
                                OneToOneField,
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                ],
            ],
            Dict[Any, Any],
        ],
        Tuple[
            List[Tuple[Expression, Optional[str], Optional[str]]],
            Dict[
                str,
                Union[
                    List[
                        Union[
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[Any],
                                    List[int],
                                    Type[User],
                                    bool,
                                    ForeignKey,
                                ],
                            ],
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[Any],
                                    List[int],
                                    Type[ContentType],
                                    bool,
                                    ForeignKey,
                                ],
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                ],
            ],
            Dict[str, int],
        ],
        Tuple[
            List[Tuple[Expression, Tuple[str, List[int]], Optional[str]]],
            Dict[
                str,
                Union[
                    List[
                        Union[
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[Any],
                                    List[int],
                                    Type[Model],
                                    bool,
                                    ForeignKey,
                                ],
                            ],
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Callable,
                                                List[Any],
                                                List[int],
                                                Type[Model],
                                                bool,
                                                ForeignKey,
                                            ],
                                        ]
                                    ],
                                    List[int],
                                    Type[Model],
                                    bool,
                                    ForeignKey,
                                ],
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                ],
            ],
            Dict[str, int],
        ],
        Tuple[List[Tuple[Expression, str, str]], None, Dict[str, int]],
        Tuple[
            List[
                Union[
                    Tuple[Col, Tuple[str, List[Any]], None],
                    Tuple[RawSQL, Tuple[str, List[Any]], str],
                ]
            ],
            Dict[
                str,
                Union[
                    List[
                        Dict[
                            str,
                            Union[
                                Callable,
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Callable,
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Callable,
                                                        List[
                                                            Dict[
                                                                str,
                                                                Union[
                                                                    Callable,
                                                                    List[
                                                                        Dict[
                                                                            str,
                                                                            Union[
                                                                                Callable,
                                                                                List[
                                                                                    Any
                                                                                ],
                                                                                List[
                                                                                    int
                                                                                ],
                                                                                Type[
                                                                                    Model
                                                                                ],
                                                                                bool,
                                                                                ForeignKey,
                                                                            ],
                                                                        ]
                                                                    ],
                                                                    List[int],
                                                                    Type[Model],
                                                                    bool,
                                                                    ForeignKey,
                                                                ],
                                                            ]
                                                        ],
                                                        List[int],
                                                        Type[Model],
                                                        bool,
                                                        ForeignKey,
                                                    ],
                                                ]
                                            ],
                                            List[int],
                                            Type[Model],
                                            bool,
                                            ForeignKey,
                                        ],
                                    ]
                                ],
                                List[int],
                                Type[Model],
                                bool,
                                ForeignKey,
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                ],
            ],
            Dict[str, int],
        ],
        Tuple[None, Dict[str, int], Dict[str, int]],
    ]: ...
    def get_order_by(
        self
    ) -> List[
        Tuple[
            OrderBy,
            Union[
                Tuple[str, List[Any], bool],
                Tuple[str, List[Union[int, str]], bool],
                Tuple[str, List[int], bool],
                Tuple[str, List[str], bool],
                Tuple[str, Tuple, bool],
            ],
        ]
    ]: ...
    def get_extra_select(
        self,
        order_by: List[
            Tuple[
                OrderBy,
                Union[
                    Tuple[str, List[Any], bool],
                    Tuple[str, List[Union[int, str]], bool],
                    Tuple[str, List[int], bool],
                    Tuple[str, List[str], bool],
                    Tuple[str, Tuple, bool],
                ],
            ]
        ],
        select: List[Tuple[Expression, Optional[str], Optional[str]]],
    ) -> List[Tuple[OrderBy, Tuple[str, List[Any]], None]]: ...
    def quote_name_unless_alias(self, name: str) -> str: ...
    def compile(
        self,
        node: Union[
            Combinable,
            OrderBy,
            Lookup,
            FilteredRelation,
            QueryWrapper,
            BaseTable,
            Join,
            Query,
            ExtraWhere,
            NothingNode,
            SubqueryConstraint,
            WhereNode,
        ],
        select_format: Any = ...,
    ) -> Tuple[
        str,
        Union[
            List[Optional[int]],
            List[Union[date, int]],
            List[Union[date, str]],
            List[Union[Decimal, int]],
            List[Union[float, int]],
            List[Union[int, memoryview]],
            List[Union[int, str]],
            Tuple,
        ],
    ]: ...
    def get_combinator_sql(
        self, combinator: str, all: bool
    ) -> Tuple[List[str], Union[List[int], List[str]]]: ...
    def as_sql(
        self, with_limits: bool = ..., with_col_aliases: bool = ...
    ) -> Any: ...
    def get_default_columns(
        self,
        start_alias: Optional[str] = ...,
        opts: Optional[Options] = ...,
        from_parent: Optional[Type[Model]] = ...,
    ) -> List[Col]: ...
    def get_distinct(self) -> Tuple[List[Any], List[Any]]: ...
    def find_ordering_name(
        self,
        name: str,
        opts: Options,
        alias: Optional[str] = ...,
        default_order: str = ...,
        already_seen: Optional[
            Union[
                Set[
                    Tuple[
                        None,
                        Tuple[Tuple[str, str]],
                        Tuple[Tuple[str, str]],
                        Tuple[Tuple[str, str]],
                    ]
                ],
                Set[Tuple[Tuple[Tuple[str, str]], Tuple[Tuple[str, str]]]],
            ]
        ] = ...,
    ) -> List[Tuple[OrderBy, bool]]: ...
    def get_from_clause(self) -> Tuple[List[str], List[Union[int, str]]]: ...
    def get_related_selections(
        self,
        select: List[Tuple[Expression, Optional[str]]],
        opts: Optional[Options] = ...,
        root_alias: Optional[str] = ...,
        cur_depth: int = ...,
        requested: Optional[
            Union[Dict[str, Dict[str, Dict[str, Dict[Any, Any]]]], bool]
        ] = ...,
        restricted: Optional[bool] = ...,
    ) -> Union[
        List[
            Dict[
                str,
                Union[
                    Callable,
                    List[
                        Dict[
                            str,
                            Union[
                                Callable,
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Callable,
                                            List[Any],
                                            List[int],
                                            Type[Model],
                                            bool,
                                            OneToOneField,
                                        ],
                                    ]
                                ],
                                List[int],
                                Type[Model],
                                bool,
                                OneToOneField,
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                    bool,
                    FieldCacheMixin,
                ],
            ]
        ],
        List[
            Dict[
                str,
                Union[
                    Callable,
                    List[
                        Dict[
                            str,
                            Union[
                                Callable,
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Callable,
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Callable,
                                                        List[
                                                            Dict[
                                                                str,
                                                                Union[
                                                                    Callable,
                                                                    List[Any],
                                                                    List[int],
                                                                    Type[Model],
                                                                    bool,
                                                                    ForeignKey,
                                                                ],
                                                            ]
                                                        ],
                                                        List[int],
                                                        Type[Model],
                                                        bool,
                                                        ForeignKey,
                                                    ],
                                                ]
                                            ],
                                            List[int],
                                            Type[Model],
                                            bool,
                                            ForeignKey,
                                        ],
                                    ]
                                ],
                                List[int],
                                Type[Model],
                                bool,
                                ForeignKey,
                            ],
                        ]
                    ],
                    List[int],
                    Type[Model],
                    bool,
                    ForeignKey,
                ],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Callable,
                        List[Any],
                        List[int],
                        Type[User],
                        bool,
                        ForeignKey,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Callable,
                        List[Any],
                        List[int],
                        Type[ContentType],
                        bool,
                        ForeignKey,
                    ],
                ],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Callable,
                        List[Any],
                        List[int],
                        Type[Model],
                        bool,
                        ForeignKey,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Callable,
                        List[
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[Any],
                                    List[int],
                                    Type[Model],
                                    bool,
                                    ForeignKey,
                                ],
                            ]
                        ],
                        List[int],
                        Type[Model],
                        bool,
                        FieldCacheMixin,
                    ],
                ],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Callable,
                        List[Any],
                        List[int],
                        Type[Model],
                        bool,
                        ForeignKey,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Callable,
                        List[
                            Union[
                                Dict[
                                    str,
                                    Union[
                                        Callable,
                                        List[Any],
                                        List[int],
                                        Type[Model],
                                        bool,
                                        ForeignKey,
                                    ],
                                ],
                                Dict[
                                    str,
                                    Union[
                                        Callable,
                                        List[Any],
                                        List[int],
                                        Type[Model],
                                        bool,
                                        OneToOneField,
                                    ],
                                ],
                            ]
                        ],
                        List[int],
                        Type[Model],
                        bool,
                        ForeignObject,
                    ],
                ],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Callable,
                        List[
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Callable,
                                                List[Any],
                                                List[int],
                                                Type[Model],
                                                bool,
                                                ForeignKey,
                                            ],
                                        ]
                                    ],
                                    List[int],
                                    Type[Model],
                                    bool,
                                    ForeignKey,
                                ],
                            ]
                        ],
                        List[int],
                        Type[Model],
                        bool,
                        ForeignKey,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Callable,
                        List[
                            Dict[
                                str,
                                Union[
                                    Callable,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Callable,
                                                List[
                                                    Dict[
                                                        str,
                                                        Union[
                                                            Callable,
                                                            List[Any],
                                                            List[int],
                                                            Type[Model],
                                                            bool,
                                                            ForeignKey,
                                                        ],
                                                    ]
                                                ],
                                                List[int],
                                                Type[Model],
                                                bool,
                                                ForeignKey,
                                            ],
                                        ]
                                    ],
                                    List[int],
                                    Type[Model],
                                    bool,
                                    ForeignKey,
                                ],
                            ]
                        ],
                        List[int],
                        Type[Model],
                        bool,
                        ForeignKey,
                    ],
                ],
            ]
        ],
    ]: ...
    def get_select_for_update_of_arguments(self): ...
    def deferred_to_columns(
        self
    ) -> Dict[Type[Model], Union[Set[Any], Set[str]]]: ...
    def get_converters(
        self, expressions: List[Optional[Expression]]
    ) -> Dict[int, Tuple[List[Callable], Expression]]: ...
    def apply_converters(
        self,
        rows: chain,
        converters: Dict[int, Tuple[List[Callable], Expression]],
    ) -> Iterator[
        Union[
            List[Optional[Union[bool, datetime, str, UUID]]],
            List[Optional[Union[bytes, date, int, str]]],
            List[Optional[Union[bytes, time, int, str]]],
            List[Optional[Union[bytes, timedelta, int, str]]],
            List[Optional[Union[bytes, Decimal, int, str]]],
            List[Optional[Union[bytes, float, int, str]]],
            List[Optional[Union[bytes, int, str, UUID]]],
            List[Optional[Union[date, time, int, str]]],
            List[Optional[Union[date, Decimal, float, int, str]]],
            List[Union[date, time, timedelta, int, str]],
            List[Union[datetime, time, Decimal, int, str]],
            List[Union[timedelta, Decimal, int, str]],
            List[Union[float, str, UUID]],
        ]
    ]: ...
    def results_iter(
        self,
        results: Optional[
            Union[
                Iterator[Any],
                List[
                    List[
                        Union[
                            Tuple[
                                int,
                                None,
                                str,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ],
                            Tuple[
                                int,
                                int,
                                str,
                                int,
                                int,
                                str,
                                int,
                                int,
                                str,
                                int,
                                int,
                                str,
                            ],
                        ]
                    ]
                ],
                List[
                    Union[
                        List[Tuple[Union[date, float, int, str]]],
                        List[
                            Union[Tuple[int, str, None], Tuple[int, str, str]]
                        ],
                    ]
                ],
            ]
        ] = ...,
        tuple_expected: bool = ...,
        chunked_fetch: bool = ...,
        chunk_size: int = ...,
    ) -> Union[Iterator[Any], chain, map]: ...
    def has_results(self) -> bool: ...
    def execute_sql(
        self,
        result_type: str = ...,
        chunked_fetch: bool = ...,
        chunk_size: int = ...,
    ) -> Optional[Union[Iterator[Any], CursorWrapper]]: ...
    def as_subquery_condition(
        self, alias: str, columns: List[str], compiler: SQLCompiler
    ) -> Tuple[str, Tuple]: ...
    def explain_query(self) -> Iterator[str]: ...

class SQLInsertCompiler(SQLCompiler):
    return_id: bool = ...
    def field_as_sql(
        self,
        field: Optional[Field],
        val: Optional[Union[Lower, float, int, memoryview, str]],
    ) -> Tuple[
        str,
        Union[List[None], List[float], List[int], List[memoryview], List[str]],
    ]: ...
    def prepare_value(
        self,
        field: Field,
        value: Optional[
            Union[
                Dict[str, Dict[str, List[str]]],
                bytes,
                date,
                time,
                timedelta,
                Decimal,
                Model,
                SQLiteNumericMixin,
                files.FieldFile,
                float,
                int,
                memoryview,
                str,
                UUID,
            ]
        ],
    ) -> Optional[Union[Lower, float, int, memoryview, str]]: ...
    def pre_save_val(
        self, field: Field, obj: Model
    ) -> Optional[
        Union[
            Dict[str, Dict[str, List[str]]],
            bytes,
            date,
            time,
            timedelta,
            Decimal,
            Model,
            SQLiteNumericMixin,
            files.FieldFile,
            float,
            int,
            memoryview,
            str,
            UUID,
        ]
    ]: ...
    def assemble_as_sql(
        self,
        fields: Union[List[None], List[Field], ImmutableList],
        value_rows: List[
            Union[
                List[Optional[Union[Lower, int]]],
                List[Optional[Union[float, int, memoryview, str]]],
            ]
        ],
    ) -> Union[
        Tuple[List[Any], List[Any]],
        Tuple[
            Tuple[Tuple[str]],
            List[List[Optional[Union[float, int, memoryview, str]]]],
        ],
    ]: ...
    def as_sql(
        self
    ) -> List[
        Tuple[
            str,
            Union[
                List[Any],
                List[None],
                List[Optional[Union[bool, str]]],
                List[Optional[Union[bool, str]]],
                List[Optional[Union[float, int, str]]],
                List[Optional[Union[int, memoryview, str]]],
                List[Optional[Union[int, str]]],
                List[Optional[Union[int, str]]],
                List[Optional[Union[int, str]]],
                List[Optional[bool]],
                List[Optional[int]],
                List[Optional[int]],
                List[Optional[str]],
                List[Optional[str]],
                List[Union[bool, str]],
                List[Union[float, int, str]],
                List[Union[float, int]],
                List[Union[float, str]],
                List[Union[float, str]],
                List[Union[int, str]],
                List[bool],
                List[float],
                List[int],
                List[memoryview],
                List[str],
                Tuple,
            ],
        ]
    ]: ...
    def execute_sql(self, return_id: Optional[bool] = ...) -> Any: ...

class SQLDeleteCompiler(SQLCompiler):
    def as_sql(self) -> Tuple[str, Tuple]: ...

class SQLUpdateCompiler(SQLCompiler):
    def as_sql(self) -> Tuple[str, Tuple]: ...
    def execute_sql(self, result_type: str) -> int: ...
    def pre_sql_setup(self) -> None: ...

class SQLAggregateCompiler(SQLCompiler):
    col_count: Any = ...
    def as_sql(self) -> Tuple[str, Tuple]: ...

def cursor_iter(
    cursor: CursorWrapper,
    sentinel: List[Any],
    col_count: Optional[int],
    itersize: int,
) -> Iterator[List[Tuple[Optional[Union[date, float, int, str]]]]]: ...
