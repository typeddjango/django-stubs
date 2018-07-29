from typing import (
    Tuple,
    Union,
)


class Loader:
    def get_dirs(self) -> Union[Tuple[str, str, str, str], Tuple[str, str, str], Tuple[str], Tuple[str, str]]: ...