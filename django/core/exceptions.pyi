from django.forms.utils import ErrorDict
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)


class ValidationError:
    def __init__(self, message: Any, code: Optional[str] = ..., params: Any = ...) -> None: ...
    def __iter__(self) -> Iterator[Union[str, Tuple[str, List[str]]]]: ...
    def __str__(self) -> str: ...
    @property
    def message_dict(self) -> Dict[str, List[str]]: ...
    @property
    def messages(self) -> List[str]: ...
    def update_error_dict(
        self,
        error_dict: Union[Dict[str, List[ValidationError]], ErrorDict]
    ) -> Union[Dict[str, List[ValidationError]], ErrorDict]: ...