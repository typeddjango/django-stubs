from collections import OrderedDict
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    Union,
    overload,
)

from psycopg2._psycopg import ReplicationConnection as _replicationConnection
from psycopg2._psycopg import ReplicationCursor as _replicationCursor
from psycopg2._range import DateRange as DateRange
from psycopg2._range import DateTimeTZRange as DateTimeTZRange
from psycopg2._range import NumericRange as NumericRange
from psycopg2._range import Range as Range
from psycopg2.extensions import _SQLType
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from typing_extensions import Literal, Protocol

class DictCursorBase(_cursor):
    _query_executed: bool
    _prefetch: bool
    row_factory: Any
    def __init__(
        self, *args: Any, row_factory: Optional[Any], **kwargs: Any
    ) -> None: ...
    def fetchone(self) -> Optional[Tuple[Any, ...]]: ...
    def fetchmany(self, size: Optional[int] = ...) -> List[Tuple[Any, ...]]: ...
    def fetchall(self) -> List[Tuple[Any, ...]]: ...
    def __iter__(self) -> Iterator[Tuple[Any, ...]]: ...

class DictConnection(_connection):
    def cursor(
        self, *args: Any, cursor_factory: Optional[DictCursorBase] = ..., **kwargs: Any
    ) -> _cursor: ...

class DictCursor(DictCursorBase):
    index: OrderedDict[str, int]
    _query_executed: bool
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def execute(
        self,
        query: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        parameters: Union[Sequence[_SQLType], Mapping[str, _SQLType]] = ...,
    ) -> None: ...

class DictRow(List[Any]):
    _index: OrderedDict[str, int]
    def __init__(self, cursor: DictCursor) -> None: ...
    def __getitem__(self, x: Union[str, int, slice]) -> Any: ...
    def __setitem__(self, x: Union[str, int, slice], v: Any) -> None: ...
    def items(self) -> Iterator[Tuple[str, Any]]: ...
    def keys(self) -> Iterator[str]: ...
    def values(self) -> Iterator[Any]: ...
    def get(
        self, x: Union[str, int, slice], default: Optional[Any] = ...
    ) -> Optional[Any]: ...
    def copy(self) -> OrderedDict[str, Any]: ...  # type: ignore [override]
    def __contains__(self, x: str) -> bool: ...  # type: ignore [override]
    def __getstate__(self) -> Tuple[Any, OrderedDict[str, int]]: ...
    def __setstate__(self, data: Tuple[Any, OrderedDict[str, int]]) -> None: ...

class RealDictConnection(_connection):
    def cursor(  # type: ignore [override]
        self, *args: Any, cursor_factory: RealDictCursor, **kwargs: Any
    ) -> _cursor: ...

class RealDictCursor(DictCursorBase):
    column_mapping: List[Any]
    _query_executed: bool
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def execute(
        self,
        query: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...

class RealDictRow(OrderedDict[Any, Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...

class NamedTupleConnection(_connection):
    def cursor(self, *args: Any, **kwargs: Any) -> _cursor: ...

class NamedTupleCursor(_cursor):
    Record: Optional[NamedTuple] = ...
    MAX_CACHE: int = ...
    def execute(
        self,
        query: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def executemany(
        self,
        query: str,
        vars_list: Sequence[Union[Sequence[_SQLType], Mapping[str, _SQLType]]],
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def fetchone(self) -> Optional[Tuple[Any, ...]]: ...
    def fetchmany(self, size: int = ...) -> List[Tuple[Any, ...]]: ...
    def fetchall(self) -> List[Tuple[Any, ...]]: ...
    def __iter__(self) -> Iterator[Tuple[Any, ...]]: ...

class LoggingConnection(_connection):
    def initialize(self, logobj: Any) -> None: ...
    def filter(self, msg: Any, curs: Any) -> Any: ...
    def cursor(self, *args: Any, **kwargs: Any) -> _cursor: ...

class LoggingCursor(_cursor):
    def execute(
        self,
        query: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...

class MinTimeLoggingConnection(LoggingConnection):
    def initialize(self, logobj: Any, mintime: int = ...) -> None: ...
    def filter(self, msg: Any, curs: Any) -> Optional[str]: ...
    def cursor(self, *args: Any, **kwargs: Any) -> _cursor: ...

class MinTimeLoggingCursor(LoggingCursor):
    timestamp: float
    def execute(
        self,
        query: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def callproc(
        self,
        procname: str,
        vars: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...

class LogicalReplicationConnection(_replicationConnection):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class PhysicalReplicationConnection(_replicationConnection):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class StopReplication(Exception):
    pass

class ReplicationCursor(_replicationCursor):
    def create_replication_slot(
        self,
        slot_name: Any,
        slot_type: Optional[Any] = ...,
        output_plugin: Optional[Any] = ...,
    ) -> None: ...
    def drop_replication_slot(self, slot_name: Any) -> None: ...
    def start_replication(
        self,
        slot_name: Optional[Any] = ...,
        slot_type: Optional[Any] = ...,
        start_lsn: int = ...,
        timeline: int = ...,
        options: Optional[Mapping[Any, Any]] = ...,
        decode: bool = ...,
    ) -> None: ...
    def fileno(self) -> Any: ...

class UUID_adapter:
    _uuid: Any
    def __init__(self, uuid: Any) -> None: ...
    def __conform__(self, proto: Any) -> Optional[UUID_adapter]: ...
    def getquoted(self) -> str: ...

def register_uuid(
    oids: Optional[Any] = ..., conn_or_curs: Union[_cursor, _connection, None] = ...
) -> None: ...

class Inet:
    addr: Any
    _conn: _connection
    def __init__(self, addr: Any) -> None: ...
    def prepare(self, conn: _connection) -> None: ...
    def getquoted(self) -> bytes: ...
    def __conform__(self, proto: Any) -> Optional[Inet]: ...

def register_inet(
    oid: Optional[int] = ..., conn_or_curs: Optional[Union[_connection, _cursor]] = ...
) -> Inet: ...
def wait_select(conn: _connection) -> None: ...

class HstoreAdapter:
    wrapped: Any
    conn: _connection
    def __init__(self, wrapped: Any) -> None: ...
    def prepare(self, conn: _connection) -> None: ...
    def _getquoted_9(self) -> bytes: ...
    getquoted = _getquoted_9
    @classmethod
    def parse(
        cls, s: Optional[str], cur: _cursor, _bsdec: Pattern[str] = ...
    ) -> Optional[Dict[str, str]]: ...
    @classmethod
    def parse_unicode(
        cls, s: Optional[str], cur: _cursor
    ) -> Optional[Dict[str, str]]: ...
    @classmethod
    def get_oids(
        cls, conn_or_curs: Union[_connection, _cursor]
    ) -> Tuple[Tuple[Any, ...], Tuple[Any, ...]]: ...

def register_hstore(
    conn_or_curs: Union[_connection, _cursor],
    globally: bool = ...,
    unicode: bool = ...,
    oid: Optional[int] = ...,
    array_oid: Optional[int] = ...,
) -> None: ...

class CompositeCaster:
    name: str
    schema: Optional[Any]
    oid: int
    array_oid: Optional[int]
    attrnames: List[Any]
    attrtypes: List[Any]
    typecaster: Any
    array_typecaster: Optional[Any]
    def __init__(
        self,
        name: str,
        oid: int,
        attrs: Any,
        array_oid: Optional[int] = ...,
        schema: Optional[Any] = ...,
    ) -> None: ...
    def parse(self, s: Optional[str], curs: Any) -> Any: ...
    def make(self, values: Any) -> Any: ...
    @classmethod
    def tokenize(cls, s: str) -> List[Optional[str]]: ...

def register_composite(
    name: str,
    conn_or_curs: Union[_connection, _cursor],
    globally: bool = ...,
    factory: Optional[CompositeCaster] = ...,
) -> CompositeCaster: ...

class _CursorLike(Protocol):
    @property
    def connection(self) -> _connection: ...
    def mogrify(
        self,
        operation: str,
        parameters: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> bytes: ...
    def execute(
        self,
        sql: str,
        params: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> None: ...
    def fetchall(self) -> List[Tuple[Any, ...]]: ...

def execute_batch(
    cur: _CursorLike,
    sql: str,
    argslist: Sequence[Union[Sequence[_SQLType], Mapping[str, _SQLType]]],
    page_size: int = ...,
) -> None: ...
@overload
def execute_values(
    cur: _CursorLike,
    sql: str,
    argslist: Sequence[Union[Sequence[_SQLType], Mapping[str, _SQLType]]],
    *,
    template: Optional[bytes] = ...,
    page_size: int = ...,
    fetch: Literal[True],
) -> List[Tuple[Any, ...]]: ...
@overload
def execute_values(
    cur: _CursorLike,
    sql: str,
    argslist: Sequence[Union[Sequence[_SQLType], Mapping[str, _SQLType]]],
    *,
    template: Optional[bytes] = ...,
    page_size: int = ...,
    fetch: Literal[False] = ...,
) -> None: ...
