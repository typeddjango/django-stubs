from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import (
    IO,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from uuid import UUID

from typing_extensions import Literal

ISOLATION_LEVEL_AUTOCOMMIT: Literal[0]
ISOLATION_LEVEL_READ_UNCOMMITTED: Literal[4]
ISOLATION_LEVEL_READ_COMMITTED: Literal[1]
ISOLATION_LEVEL_REPEATABLE_READ: Literal[2]
ISOLATION_LEVEL_SERIALIZABLE: Literal[3]
ISOLATION_LEVEL_DEFAULT: None

STATUS_SETUP: Literal[0]
STATUS_READY: Literal[1]
STATUS_BEGIN: Literal[2]
STATUS_SYNC: Literal[3]
STATUS_ASYNC: Literal[4]
STATUS_PREPARED: Literal[5]

STATUS_IN_TRANSACTION: Literal[2]

POLL_OK: Literal[0]
POLL_READ: Literal[1]
POLL_WRITE: Literal[2]
POLL_ERROR: Literal[3]

_PollConstants = Literal[0, 1, 2, 3]

TRANSACTION_STATUS_IDLE: Literal[0]
TRANSACTION_STATUS_ACTIVE: Literal[1]
TRANSACTION_STATUS_INTRANS: Literal[2]
TRANSACTION_STATUS_INERROR: Literal[3]
TRANSACTION_STATUS_UNKNOWN: Literal[4]

_TransactionStatus = Literal[0, 1, 2, 3, 4]

_Mixed = Union[None, bool, int, float, Decimal, str, bytes, datetime, UUID]
_SQLType = Union[_Mixed, Sequence[_Mixed], Mapping[str, _Mixed]]

class cursor:
    def __init__(self, conn: _connection) -> None: ...
    @property
    def description(self) -> Optional[Tuple[Column, ...]]: ...
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    @property
    def connection(self) -> _connection: ...
    @property
    def name(self) -> Optional[str]: ...
    scrollable: Optional[bool]
    withhold: bool
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
        parameters: Union[Sequence[_SQLType], Mapping[str, _SQLType]] = ...,
    ) -> None: ...
    def mogrify(
        self,
        operation: str,
        parameters: Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]] = ...,
    ) -> bytes: ...
    def setinputsizes(self, sizes: int) -> None: ...
    def fetchone(self) -> Optional[Tuple[Any, ...]]: ...
    def fetchmany(self, size: int = ...) -> List[Tuple[Any, ...]]: ...
    def fetchall(self) -> List[Tuple[Any, ...]]: ...
    def scroll(
        self, value: int, mode: Union[Literal["relative"], Literal["absolute"]] = ...
    ) -> None: ...
    arraysize: int
    itersize: int
    @property
    def rowcount(self) -> int: ...
    @property
    def rownumber(self) -> int: ...
    @property
    def lastrowid(self) -> Optional[int]: ...
    @property
    def query(self) -> Optional[str]: ...
    @property
    def statusmessage(self) -> Optional[str]: ...
    def cast(self, oid: int, s: str) -> Any: ...
    tzinfo_factory: Any
    def nextset(self) -> None: ...
    def setoutputsize(self, size: int, column: int = ...) -> None: ...
    def copy_from(
        self,
        file: IO[str],
        table: str,
        sep: str = ...,
        null: str = ...,
        size: int = ...,
        columns: Optional[Iterable[str]] = ...,
    ) -> None: ...
    def copy_to(
        self,
        file: IO[str],
        table: str,
        sep: str = ...,
        null: str = ...,
        columns: Optional[str] = ...,
    ) -> None: ...
    def copy_expert(self, sql: str, file: IO[str], size: int = ...) -> None: ...
    def __enter__(self) -> cursor: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...
    def __iter__(self) -> Iterator[Tuple[Any, ...]]: ...
    def __next__(self) -> Tuple[Any, ...]: ...

_cursor = cursor
_IsolationLevelsCodes = Literal[0, 1, 2, 3, 4]

_IsolationLevels = Literal[
    "READ UNCOMMIITED",
    "READ COMMITTED",
    "REPEATABLE READ",
    "SERIALIZABLE",
    _IsolationLevelsCodes,
]

class connection:
    def __init__(self, dsn: str) -> None: ...
    def cursor(
        self,
        name: Optional[str] = ...,
        cursor_factory: Optional[Any] = ...,
        scrollable: Optional[bool] = ...,
        withhold: bool = ...,
    ) -> _cursor: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...
    def xid(self, format_id: str, gtrid: str, bqual: Any) -> Xid: ...
    def tpc_begin(self, xid: Union[str, Xid]) -> None: ...
    def tpc_preparse(self) -> None: ...
    def tpc_commit(self, xid: Union[str, Xid] = ...) -> None: ...
    def tpc_rollback(self, xid: Union[str, Xid] = ...) -> None: ...
    def tpc_recover(self) -> None: ...
    @property
    def closed(self) -> int: ...
    def cancel(self) -> None: ...
    def reset(self) -> None: ...
    @property
    def dsn(self) -> str: ...
    def set_session(
        self,
        isolation_level: Optional[_IsolationLevels] = ...,
        readonly: Optional[bool] = ...,
        deferrable: Optional[bool] = ...,
        autocommit: Optional[bool] = ...,
    ) -> None: ...
    autocommit: bool
    isolation_level: _IsolationLevelsCodes
    readonly: Optional[bool]
    deferrable: Optional[bool]
    def set_isolation_level(self, level: _IsolationLevelsCodes) -> None: ...
    encoding: str
    def set_client_encoding(self, enc: str) -> None: ...
    @property
    def notices(self) -> List[str]: ...
    notifies: List[Notify]
    cursor_factory: Any
    info: ConnectionInfo
    @property
    def status(self) -> int: ...
    def lobject(
        self,
        oid: int = ...,
        mode: str = ...,
        new_oid: int = ...,
        new_file: Any = ...,
        lobject_factory: Any = ...,
    ) -> _lobject: ...
    @property
    def async_(self) -> Literal[0, 1]: ...
    def poll(self) -> _PollConstants: ...
    def fileno(self) -> Any: ...
    def isexecuting(self) -> bool: ...
    pgconn_ptr: Any
    def get_native_connection(self) -> Any: ...
    def get_transaction_status(self) -> _TransactionStatus: ...
    @property
    def protocol_version(self) -> int: ...
    @property
    def server_version(self) -> int: ...
    def get_backend_pid(self) -> int: ...
    def get_parameter_status(self, parameter: str) -> Optional[str]: ...
    def get_dsn_parameters(self) -> Dict[str, str]: ...
    def __enter__(self) -> connection: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...

class Xid: ...
class lobject: ...

_lobject = lobject

class Notify:
    def __init__(self, pid: str, channel: str, payload: str) -> None: ...
    channel: str
    payload: str
    pid: str

_connection = connection

class ConnectionInfo:
    def __init__(self, connection: connection) -> None: ...
    dbname: str
    user: str
    password: str
    host: str
    port: int
    options: str
    dsn_parameters: Dict[str, str]
    status: int
    transaction_status: int
    def parameter_status(self, name: str) -> str: ...
    protocol_version: int
    server_version: int
    error_message: Optional[str]
    socket: int
    backend_pid: int
    needs_password: bool
    used_password: bool
    ssl_in_use: bool
    def ssl_attribute(self, name: str) -> str: ...
    ssl_attribute_names: List[str]

class Column(NamedTuple):
    name: Optional[str]
    type_code: Optional[int]
    display_size: Optional[int]
    internal_size: Optional[int]
    precision: Optional[int]
    scale: Optional[int]
    null_ok: None
    table_column: Optional[str]
    table_oid: Optional[int]

class Diagnostics:
    @property
    def column_name(self) -> Optional[str]: ...
    @property
    def constraint_name(self) -> Optional[str]: ...
    @property
    def context(self) -> Optional[str]: ...
    @property
    def datatype_name(self) -> Optional[str]: ...
    @property
    def internal_position(self) -> Optional[str]: ...
    @property
    def internal_query(self) -> Optional[str]: ...
    @property
    def message_detail(self) -> Optional[str]: ...
    @property
    def message_hint(self) -> Optional[str]: ...
    @property
    def message_primary(self) -> Optional[str]: ...
    @property
    def schema_name(self) -> Optional[str]: ...
    @property
    def severity(self) -> Optional[str]: ...
    @property
    def severity_nonlocalized(self) -> Optional[str]: ...
    @property
    def source_file(self) -> Optional[str]: ...
    @property
    def source_function(self) -> Optional[str]: ...
    @property
    def source_line(self) -> Optional[str]: ...
    @property
    def sqlstate(self) -> Optional[str]: ...
    @property
    def statement_position(self) -> Optional[str]: ...
    @property
    def table_name(self) -> Optional[str]: ...

def parse_dsn(dsn: str) -> Dict[str, str]: ...
def quote_ident(str: str, scope: Union[connection, cursor]) -> str: ...
def encrypt_password(
    password: str,
    user: str,
    scope: Optional[Union[connection, cursor]] = ...,
    algorithm: Optional[str] = ...,
) -> str: ...
