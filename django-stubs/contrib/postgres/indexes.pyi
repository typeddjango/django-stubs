from typing import Any, Optional

from django.db.models import Index

class PostgresIndex(Index):
    @property
    def max_name_length(self) -> int: ...

class BrinIndex(PostgresIndex):
    def __init__(
        self, *, autosummarize: Optional[bool] = ..., pages_per_range: Optional[int] = ..., **kwargs: Any
    ) -> None: ...

class BTreeIndex(PostgresIndex):
    def __init__(self, *, fillfactor: Optional[int] = ..., **kwargs: Any): ...

class GinIndex(PostgresIndex):
    def __init__(
        self, *, fastupdate: Optional[bool] = ..., gin_pending_list_limit: Optional[int] = ..., **kwargs: Any
    ) -> None: ...

class GistIndex(PostgresIndex):
    def __init__(self, *, buffering: Optional[bool] = ..., fillfactor: Optional[int] = ..., **kwargs: Any) -> None: ...

class HashIndex(PostgresIndex):
    def __init__(self, *, fillfactor: Optional[int] = ..., **kwargs: Any) -> None: ...

class SpGistIndex(PostgresIndex):
    def __init__(self, *, fillfactor: Optional[int] = ..., **kwargs: Any) -> None: ...
