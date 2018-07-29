from io import BufferedRandom
from typing import Union


def _fd(f: Union[BufferedRandom, int]) -> int: ...


def lock(f: Union[BufferedRandom, int], flags: int) -> bool: ...


def unlock(f: int) -> bool: ...