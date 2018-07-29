from typing import (
    Optional,
    Union,
)


class DictWrapper:
    def __getitem__(self, key: str) -> Optional[Union[str, int]]: ...