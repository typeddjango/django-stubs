from typing import IO, Optional, Tuple, Union

from django.core.files import File
from django.utils._os import _PathCompatible

class ImageFile(File[bytes]):
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...

def get_image_dimensions(
    file_or_path: Union[_PathCompatible, IO[bytes]], close: bool = ...
) -> Tuple[Optional[int], Optional[int]]: ...
