from typing import Optional, Sequence, Union

from django.db.models.query_utils import Q

from django.db.models import Index, Func
from django.db.models.expressions import BaseExpression, Combinable

class PostgresIndex(Index): ...

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
