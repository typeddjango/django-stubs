from _frozen_importlib_external import _NamespacePath
from typing import (
    List,
    Optional,
    Union,
)


class _SixMetaPathImporter:
    def find_module(
        self,
        fullname: str,
        path: Optional[Union[List[str], _NamespacePath]] = ...
    ) -> None: ...