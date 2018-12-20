from ctypes import Structure, c_int64, c_ulong, c_void_p
from io import BufferedRandom, TextIOWrapper
from typing import Union

LOCK_SH: int
LOCK_NB: int
LOCK_EX: int
ULONG_PTR = c_int64
ULONG_PTR = c_ulong
PVOID = c_void_p

class _OFFSET(Structure): ...
class _OFFSET_UNION(Union): ...
class OVERLAPPED(Structure): ...

def lock(f: Union[BufferedRandom, TextIOWrapper, int], flags: int) -> bool: ...
def unlock(f: Union[BufferedRandom, int]) -> bool: ...
