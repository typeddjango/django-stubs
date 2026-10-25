from __future__ import annotations

from typing import assert_type

from django.utils.deconstruct import deconstructible


@deconstructible
class Bare:
    def __init__(self, x: int) -> None: ...


@deconstructible(path="app.WithPath")
class WithPath:
    def __init__(self, x: int) -> None: ...


assert_type(Bare(1), Bare)
assert_type(WithPath(1), WithPath)
