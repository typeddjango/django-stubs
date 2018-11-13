from typing import Any


class ModelBase(type):
    pass


class Model(metaclass=ModelBase):
    class DoesNotExist(Exception):
        pass

    def __init__(self, **kwargs) -> None: ...

    def delete(self,
               using: Any = ...,
               keep_parents: bool = ...) -> None: ...