from typing import Optional, Tuple

from django.template import Engine

from .filesystem import Loader as FilesystemLoader

class Loader(FilesystemLoader):
    dirs: None
    engine: Engine
    def get_dirs(self) -> Tuple: ...
