from django.core.checks.messages import Warning
from typing import (
    Callable,
    List,
    Optional,
    Union,
)


class CheckRegistry:
    def __init__(self) -> None: ...
    def get_checks(self, include_deployment_checks: bool = ...) -> List[Callable]: ...
    def register(self, check: Union[str, Callable] = ..., *tags, **kwargs) -> Callable: ...
    def run_checks(
        self,
        app_configs: None = ...,
        tags: Optional[List[str]] = ...,
        include_deployment_checks: bool = ...
    ) -> Union[List[str], List[Warning], List[int]]: ...
    def tag_exists(self, tag: str, include_deployment_checks: bool = ...) -> bool: ...