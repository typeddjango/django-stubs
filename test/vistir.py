# Borrowed from Pew.
# See https://github.com/berdario/pew/blob/master/pew/_utils.py#L82
import os
import sys
from pathlib import Path

from decorator import contextmanager


@contextmanager
def temp_environ():
    """Allow the ability to set os.environ temporarily"""
    environ = dict(os.environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(environ)


@contextmanager
def temp_path():
    """A context manager which allows the ability to set sys.path temporarily"""
    path = [p for p in sys.path]
    try:
        yield
    finally:
        sys.path = [p for p in path]


@contextmanager
def cd(path):
    """Context manager to temporarily change working directories"""
    if not path:
        return
    prev_cwd = Path.cwd().as_posix()
    if isinstance(path, Path):
        path = path.as_posix()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)
