from django.db.migrations.operations.models import CreateModel
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)


class Operation:
    @staticmethod
    def __new__(cls: Any, *args, **kwargs) -> Operation: ...
    def _get_model_tuple(self, remote_model: str, app_label: str, model_name: str) -> Tuple[str, str]: ...
    def reduce(
        self,
        operation: Operation,
        in_between: Any,
        app_label: Optional[str] = ...
    ) -> Union[bool, List[CreateModel]]: ...
    def references_field(self, model_name: str, name: str, app_label: str = ...) -> bool: ...
    def references_model(self, name: str, app_label: str = ...) -> bool: ...