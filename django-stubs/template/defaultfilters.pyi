from datetime import date, datetime, time, timedelta
from decimal import Decimal
from io import BytesIO
from sqlite3 import OperationalError
from typing import (Any, Callable, Dict, Iterator, List, Optional, Tuple, Type,
                    Union)

from django.contrib.admin.helpers import AdminErrorList
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.templatetags.admin_list import ResultList
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.views import LoginView
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadhandler import FileUploadHandler
from django.core.handlers.wsgi import WSGIRequest
from django.db.backends.sqlite3.base import (DatabaseWrapper,
                                             SQLiteCursorWrapper)
from django.db.backends.utils import CursorWrapper
from django.db.models.base import Model
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.db.utils import OperationalError
from django.http.multipartparser import LazyStream, MultiPartParser
from django.http.response import HttpResponse
from django.template.backends.django import DjangoTemplates, Template
from django.template.base import Node, Template
from django.template.context import RequestContext
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader_tags import BlockContext, BlockNode
from django.test.client import FakePayload, RequestFactory
from django.urls.resolvers import ResolverMatch, URLResolver
from django.utils.datastructures import MultiValueDict
from django.utils.feedgenerator import Enclosure, Rss201rev2Feed
from django.utils.functional import cached_property
from django.utils.safestring import SafeText
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.debug import CallableSettingWrapper, ExceptionReporter
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.dates import BaseDateDetailView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, ModelFormMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from .base import Variable, VariableDoesNotExist
from .library import Library

register: Any

def stringfilter(func: Callable) -> Callable: ...
def addslashes(value: str) -> str: ...
def capfirst(value: str) -> str: ...
def escapejs_filter(value: str) -> SafeText: ...
def json_script(value: Dict[str, str], element_id: SafeText) -> SafeText: ...
def floatformat(
    text: Optional[Union[Decimal, float, int, str]], arg: Union[int, str] = ...
) -> str: ...
def iriencode(value: str) -> str: ...
def linenumbers(value: str, autoescape: bool = ...) -> SafeText: ...
def lower(value: str) -> str: ...
def make_list(value: str) -> List[str]: ...
def slugify(value: str) -> SafeText: ...
def stringformat(value: Any, arg: str) -> str: ...
def title(value: str) -> str: ...
def truncatechars(value: str, arg: Union[SafeText, int]) -> str: ...
def truncatechars_html(value: str, arg: Union[int, str]) -> str: ...
def truncatewords(value: str, arg: Union[int, str]) -> str: ...
def truncatewords_html(value: str, arg: Union[int, str]) -> str: ...
def upper(value: str) -> str: ...
def urlencode(value: str, safe: Optional[SafeText] = ...) -> str: ...
def urlize(value: str, autoescape: bool = ...) -> SafeText: ...
def urlizetrunc(
    value: str, limit: Union[SafeText, int], autoescape: bool = ...
) -> SafeText: ...
def wordcount(value: str) -> int: ...
def wordwrap(value: str, arg: Union[SafeText, int]) -> str: ...
def ljust(value: str, arg: Union[SafeText, int]) -> str: ...
def rjust(value: str, arg: Union[SafeText, int]) -> str: ...
def center(value: str, arg: Union[SafeText, int]) -> str: ...
def cut(value: str, arg: str) -> str: ...
def escape_filter(value: str) -> SafeText: ...
def force_escape(value: str) -> SafeText: ...
def linebreaks_filter(value: str, autoescape: bool = ...) -> SafeText: ...
def linebreaksbr(value: str, autoescape: bool = ...) -> SafeText: ...
def safe(value: str) -> SafeText: ...
def safeseq(value: List[str]) -> List[SafeText]: ...
def striptags(value: str) -> str: ...
def dictsort(
    value: Union[
        Dict[str, int],
        List[Dict[str, Dict[str, Union[int, str]]]],
        List[Dict[str, Union[int, str]]],
        List[Tuple[str, str]],
        List[int],
        int,
        str,
    ],
    arg: Union[int, str],
) -> Union[
    List[Dict[str, Dict[str, Union[int, str]]]],
    List[Dict[str, Union[int, str]]],
    List[Tuple[str, str]],
    str,
]: ...
def dictsortreversed(
    value: Union[
        Dict[str, int],
        List[Dict[str, Union[int, str]]],
        List[Tuple[str, str]],
        List[int],
        int,
        str,
    ],
    arg: Union[int, str],
) -> Union[List[Dict[str, Union[int, str]]], List[Tuple[str, str]], str]: ...
def first(value: Union[List[int], List[str], str]) -> Union[int, str]: ...
def join(value: Any, arg: str, autoescape: bool = ...) -> Any: ...
def last(value: List[str]) -> str: ...
def length(
    value: Optional[
        Union[
            List[Optional[Union[Dict[Any, Any], int, str]]],
            AdminErrorList,
            QuerySet,
            int,
            str,
        ]
    ]
) -> int: ...
def length_is(
    value: Optional[
        Union[
            List[Callable],
            List[Optional[Union[Dict[Any, Any], int, str]]],
            Tuple[str, str],
            int,
            str,
        ]
    ],
    arg: Union[SafeText, int],
) -> Union[bool, str]: ...
def random(value: List[str]) -> str: ...
def slice_filter(value: Any, arg: str) -> Any: ...
def unordered_list(
    value: Union[
        Iterator[Any],
        List[Union[List[Union[List[Union[List[str], str]], str]], str]],
        List[Union[List[Union[List[str], str]], str]],
    ],
    autoescape: bool = ...,
) -> SafeText: ...
def add(
    value: Union[List[int], Tuple[int, int], date, int, str],
    arg: Union[List[int], Tuple[int, int], timedelta, int, str],
) -> Union[List[int], Tuple[int, int, int, int], date, int, str]: ...
def get_digit(value: Union[int, str], arg: int) -> Union[int, str]: ...
def date(
    value: Optional[Union[date, time, str]], arg: Optional[str] = ...
) -> str: ...
def time(
    value: Optional[Union[date, time, str]], arg: Optional[str] = ...
) -> str: ...
def timesince_filter(
    value: Optional[date], arg: Optional[date] = ...
) -> str: ...
def timeuntil_filter(
    value: Optional[date], arg: Optional[date] = ...
) -> str: ...
def default(
    value: Optional[Union[int, str]], arg: Union[int, str]
) -> Union[int, str]: ...
def default_if_none(
    value: Optional[str], arg: Union[int, str]
) -> Union[int, str]: ...
def divisibleby(value: int, arg: int) -> bool: ...
def yesno(
    value: Optional[int], arg: Optional[str] = ...
) -> Optional[Union[bool, str]]: ...
def filesizeformat(bytes_: Union[complex, int, str]) -> str: ...
def pluralize(value: Any, arg: str = ...) -> str: ...
def phone2numeric_filter(value: str) -> str: ...
def pprint(
    value: Optional[
        Union[
            Callable,
            Dict[int, None],
            Dict[
                str, Optional[Union[List[Enclosure], List[str], datetime, str]]
            ],
            Dict[str, Optional[Union[TemplateResponseMixin, int]]],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[Dict[Any, Any], Dict[str, None], int, str]
                        ],
                    ],
                    Tuple[str, Dict[str, bytes]],
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[List[str], bool, str]],
                            Dict[str, Union[List[str], str]],
                        ],
                    ],
                    Dict[
                        str,
                        Union[Dict[str, Union[List[str], str]], Dict[str, str]],
                    ],
                    date,
                    int,
                ],
            ],
            Dict[str, Union[Dict[str, str], str]],
            Dict[str, Union[Tuple[int, int], BytesIO, FakePayload, int, str]],
            Dict[
                str,
                Union[django.db.backends.base.DatabaseWrapper, CursorWrapper],
            ],
            Dict[str, bytes],
            Dict[str, Model],
            Dict[str, BlockNode],
            Exception,
            List[Callable],
            List[Dict[str, Union[Dict[str, List[str]], List[str], bool, str]]],
            List[Tuple[str, str]],
            List[ChangeList],
            List[DjangoTemplates],
            List[TemplateDoesNotExist],
            List[Enclosure],
            List[int],
            List[str],
            Tuple,
            Type[
                Union[
                    ValueError,
                    bool,
                    ResultList,
                    InclusionAdminNode,
                    LoginView,
                    OperationalError,
                    URLResolver,
                    MultiValueDict,
                    TemplateView,
                    BaseDateDetailView,
                    DetailView,
                    DeleteView,
                    ModelFormMixin,
                    MultipleObjectTemplateResponseMixin,
                    OperationalError,
                ]
            ],
            BytesIO,
            bytes,
            date,
            ModelAdmin,
            ChangeList,
            InMemoryUploadedFile,
            FileUploadHandler,
            WSGIRequest,
            django.db.backends.base.SQLiteCursorWrapper,
            CursorWrapper,
            Model,
            Options,
            QuerySet,
            LazyStream,
            MultiPartParser,
            HttpResponse,
            DjangoTemplates,
            Template,
            Node,
            Template,
            RequestContext,
            BlockContext,
            FakePayload,
            RequestFactory,
            ResolverMatch,
            URLResolver,
            Rss201rev2Feed,
            cached_property,
            SimplerXMLGenerator,
            CallableSettingWrapper,
            ExceptionReporter,
            TemplateResponseMixin,
            int,
            str,
        ]
    ]
) -> str: ...
