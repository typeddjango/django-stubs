from _frozen_importlib import FrozenImporter
from _frozen_importlib_external import SourceFileLoader
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import QueryDict
from django.http.response import (
    Http404,
    HttpResponseNotFound,
)
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


def cleanse_setting(key: Union[str, int], value: Any) -> Any: ...


def get_default_exception_reporter_filter() -> SafeExceptionReporterFilter: ...


def get_exception_reporter_filter(
    request: Optional[WSGIRequest]
) -> SafeExceptionReporterFilter: ...


def get_safe_settings() -> Dict[str, Any]: ...


def technical_404_response(
    request: WSGIRequest,
    exception: Http404
) -> HttpResponseNotFound: ...


class CallableSettingWrapper:
    def __init__(self, callable_setting: Type[object]) -> None: ...
    def __repr__(self) -> str: ...


class ExceptionReporter:
    def __init__(
        self,
        request: Optional[WSGIRequest],
        exc_type: None,
        exc_value: Optional[str],
        tb: None,
        is_email: bool = ...
    ) -> None: ...
    def _get_lines_from_file(
        self,
        filename: str,
        lineno: int,
        context_lines: int,
        loader: Optional[Union[SourceFileLoader, Type[FrozenImporter]]] = ...,
        module_name: str = ...
    ) -> Union[Tuple[int, List[str], str, List[str]], Tuple[None, List[Any], None, List[Any]], Tuple[int, List[str], str, List[Any]]]: ...
    def get_traceback_data(self) -> Dict[str, Any]: ...
    def get_traceback_frames(self) -> List[Any]: ...
    def get_traceback_html(self) -> SafeText: ...
    def get_traceback_text(self) -> SafeText: ...


class SafeExceptionReporterFilter:
    def cleanse_special_types(self, request: Optional[WSGIRequest], value: Any) -> Any: ...
    def get_cleansed_multivaluedict(
        self,
        request: WSGIRequest,
        multivaluedict: QueryDict
    ) -> QueryDict: ...
    def get_post_parameters(
        self,
        request: Optional[WSGIRequest]
    ) -> QueryDict: ...
    def is_active(self, request: Optional[WSGIRequest]) -> bool: ...