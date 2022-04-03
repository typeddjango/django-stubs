from typing import Any, List, Optional, Sequence, Tuple, Type, Union

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.ddl_references import Statement
from django.db.models import Func, Index, Model
from django.db.models.expressions import BaseExpression, Combinable
from django.db.models.query_utils import Q
from django.utils.datastructures import _ListOrTuple

class PostgresIndex(Index):
    @property
    def max_name_length(self) -> int: ...  # type: ignore
    def create_sql(
        self, model: Type[Model], schema_editor: BaseDatabaseSchemaEditor, using: str = ..., **kwargs: Any
    ) -> Statement: ...
    def check_supported(self, schema_editor: BaseDatabaseSchemaEditor) -> None: ...
    def get_with_params(self) -> Sequence[str]: ...

class BloomIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        length: Optional[int] = ...,
        columns: _ListOrTuple[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class BrinIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        autosummarize: Optional[bool] = ...,
        pages_per_range: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class BTreeIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        fillfactor: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class GinIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        fastupdate: Optional[bool] = ...,
        gin_pending_list_limit: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class GistIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        buffering: Optional[bool] = ...,
        fillfactor: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class HashIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        fillfactor: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class SpGistIndex(PostgresIndex):
    def __init__(
        self,
        *expressions: Union[BaseExpression, Combinable, str],
        fillfactor: Optional[int] = ...,
        fields: Sequence[str] = ...,
        name: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        opclasses: Sequence[str] = ...,
        condition: Optional[Q] = ...,
        include: Optional[Sequence[str]] = ...,
    ) -> None: ...

class OpClass(Func):
    def __init__(
        self,
        expression: Union[BaseExpression, Combinable, str],
        name: str,
    ) -> None: ...
