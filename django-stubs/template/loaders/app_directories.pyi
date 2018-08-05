from typing import Optional, Tuple

from .filesystem import Loader as FilesystemLoader


class Loader(FilesystemLoader):
    dirs: None
    engine: django.template.engine.Engine
    def get_dirs(self) -> Tuple: ...
