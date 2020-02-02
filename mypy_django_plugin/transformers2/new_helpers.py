from typing import Union

from mypy.nodes import TypeInfo, MypyFile


class IncompleteDefnError(Exception):
    pass


class TypeInfoNotFound(IncompleteDefnError):
    def __init__(self, fullname: str) -> None:
        super().__init__(f'It is final iteration and required type {fullname!r} is not ready yet.')


class AttributeNotFound(IncompleteDefnError):
    def __init__(self, node: Union[TypeInfo, MypyFile], attrname: str) -> None:
        super().__init__(f'Attribute {attrname!r} is not defined for the {node.fullname!r}.')


class NameNotFound(IncompleteDefnError):
    def __init__(self, name: str) -> None:
        super().__init__(f'Could not find {name!r} in the current activated namespaces')


def get_class_fullname(klass: type) -> str:
    return klass.__module__ + '.' + klass.__qualname__
