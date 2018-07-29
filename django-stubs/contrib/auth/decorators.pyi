from typing import (
    Callable,
    List,
    Optional,
    Union,
)


def login_required(
    function: Optional[Callable] = ...,
    redirect_field_name: str = ...,
    login_url: None = ...
) -> Callable: ...


def permission_required(
    perm: Union[str, List[str]],
    login_url: None = ...,
    raise_exception: bool = ...
) -> Callable: ...


def user_passes_test(
    test_func: Callable,
    login_url: Optional[str] = ...,
    redirect_field_name: str = ...
) -> Callable: ...