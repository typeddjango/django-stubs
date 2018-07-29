from contextlib import _GeneratorContextManager
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.http.response import (
    HttpResponse,
    HttpResponseBase,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)
from unittest.case import (
    _AssertRaisesContext,
    _AssertWarnsContext,
)
from unittest.runner import TextTestResult


class CheckCondition:
    def __get__(self, instance: None, cls: Any = ...) -> bool: ...
    def __init__(self, *conditions) -> None: ...


class LiveServerTestCase:
    @classmethod
    def _create_server_thread(
        cls,
        connections_override: Dict[str, DatabaseWrapper]
    ) -> LiveServerThread: ...
    @classmethod
    def _tearDownClassInternal(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...


class LiveServerThread:
    def __init__(
        self,
        host: str,
        static_handler: Type[_StaticFilesHandler],
        connections_override: Dict[str, DatabaseWrapper] = ...,
        port: int = ...
    ) -> None: ...
    def terminate(self) -> None: ...


class SimpleTestCase:
    def __call__(self, result: TextTestResult = ...) -> None: ...
    def _assertFooMessage(
        self,
        func: Callable,
        cm_attr: str,
        expected_exception: Any,
        expected_message: str,
        *args,
        **kwargs
    ) -> _GeneratorContextManager: ...
    def _assert_contains(
        self,
        response: HttpResponseBase,
        text: Union[str, bytes, int],
        status_code: int,
        msg_prefix: str,
        html: bool
    ) -> Tuple[str, int, str]: ...
    def _assert_raises_or_warns_cm(
        self,
        func: Callable,
        cm_attr: str,
        expected_exception: Any,
        expected_message: str
    ) -> Iterator[Union[_AssertRaisesContext, _AssertWarnsContext]]: ...
    def _assert_template_used(
        self,
        response: Optional[Union[str, HttpResponse]],
        template_name: Optional[str],
        msg_prefix: str
    ) -> Union[Tuple[None, List[Any], str], Tuple[str, None, str], Tuple[None, List[str], str]]: ...
    def _post_teardown(self) -> None: ...