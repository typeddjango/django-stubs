from io import BufferedReader, BytesIO
from typing import Any, Optional, Union

from django.core.files import File


class ImageFile(File):
    file: _io.BufferedReader
    mode: str
    name: str
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...

def get_image_dimensions(
    file_or_path: Union[BytesIO, BufferedReader, str, ImageFile],
    close: bool = ...,
) -> Any: ...
