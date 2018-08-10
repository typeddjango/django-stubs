from datetime import date, datetime
from io import BytesIO
from sqlite3 import OperationalError
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.templatetags.admin_list import ResultList
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.views import LoginView
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
from django.http.request import QueryDict
from django.http.response import Http404, HttpResponse
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
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.dates import BaseDateDetailView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, ModelFormMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin

DEBUG_ENGINE: Any
HIDDEN_SETTINGS: Any
CLEANSED_SUBSTITUTE: str
CURRENT_DIR: Any

class CallableSettingWrapper:
    def __init__(
        self, callable_setting: Union[Callable, Type[Any]]
    ) -> None: ...

def cleanse_setting(
    key: Union[int, str],
    value: Optional[
        Union[
            Callable,
            Dict[int, None],
            Dict[
                str,
                Optional[
                    Union[
                        Dict[
                            str,
                            Optional[
                                Union[Dict[Any, Any], Dict[str, None], int, str]
                            ],
                        ],
                        Dict[str, Union[List[str], bool, str]],
                        int,
                        str,
                    ]
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[str, Dict[str, str]],
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
                    int,
                ],
            ],
            Dict[str, Union[List[str], bool, str]],
            List[
                Dict[
                    str, Union[Dict[str, List[Tuple[str, Dict[str, str]]]], str]
                ]
            ],
            List[Dict[str, Union[Dict[str, List[str]], List[str], bool, str]]],
            List[Union[Tuple[str, str], str]],
            Type[Any],
            int,
            str,
        ]
    ],
) -> Optional[
    Union[
        Dict[int, None],
        Dict[
            str,
            Optional[
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[Dict[Any, Any], Dict[str, None], int, str]
                        ],
                    ],
                    Dict[str, Union[List[str], bool, str]],
                    int,
                    str,
                ]
            ],
        ],
        Dict[
            str,
            Union[
                Dict[str, Dict[str, str]],
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[str], bool, str]],
                        Dict[str, Union[List[str], str]],
                    ],
                ],
                Dict[
                    str, Union[Dict[str, Union[List[str], str]], Dict[str, str]]
                ],
                int,
            ],
        ],
        Dict[str, Union[List[str], bool, str]],
        List[
            Dict[str, Union[Dict[str, List[Tuple[str, Dict[str, str]]]], str]]
        ],
        List[Dict[str, Union[Dict[str, List[str]], List[str], bool, str]]],
        List[Union[Tuple[str, str], str]],
        CallableSettingWrapper,
        int,
        str,
    ]
]: ...
def get_safe_settings() -> Union[
    Dict[
        str,
        Optional[
            Union[
                Dict[Any, Any],
                Dict[
                    str,
                    Dict[
                        str,
                        Optional[
                            Union[Dict[Any, Any], Dict[str, None], int, str]
                        ],
                    ],
                ],
                Dict[str, Dict[str, str]],
                Dict[str, None],
                Dict[
                    str,
                    Union[
                        Dict[str, Dict[str, str]],
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], bool, str]],
                                Dict[str, Union[List[str], str]],
                            ],
                        ],
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], str]], Dict[str, str]
                            ],
                        ],
                        int,
                    ],
                ],
                List[Any],
                List[
                    Dict[
                        str,
                        Union[Dict[str, List[Tuple[str, Dict[str, str]]]], str],
                    ]
                ],
                List[Tuple[str, str]],
                List[str],
                int,
                str,
            ]
        ],
    ],
    Dict[
        str,
        Optional[
            Union[
                Dict[int, None],
                Dict[
                    str,
                    Dict[
                        str,
                        Optional[
                            Union[Dict[Any, Any], Dict[str, None], int, str]
                        ],
                    ],
                ],
                Dict[str, None],
                Dict[
                    str,
                    Union[
                        Dict[str, Dict[str, str]],
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], bool, str]],
                                Dict[str, Union[List[str], str]],
                            ],
                        ],
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], str]], Dict[str, str]
                            ],
                        ],
                        int,
                    ],
                ],
                Dict[str, Union[Dict[str, str], str]],
                List[
                    Dict[str, Union[Dict[str, List[str]], List[str], bool, str]]
                ],
                List[Dict[str, Union[List[Any], bool, str]]],
                List[Union[Tuple[str, str], str]],
                CallableSettingWrapper,
                int,
                str,
            ]
        ],
    ],
]: ...
def technical_500_response(
    request: Any, exc_type: Any, exc_value: Any, tb: Any, status_code: int = ...
): ...
def get_default_exception_reporter_filter() -> SafeExceptionReporterFilter: ...
def get_exception_reporter_filter(
    request: Optional[WSGIRequest]
) -> SafeExceptionReporterFilter: ...

class ExceptionReporterFilter:
    def get_post_parameters(self, request: Any): ...
    def get_traceback_frame_variables(self, request: Any, tb_frame: Any): ...

class SafeExceptionReporterFilter(ExceptionReporterFilter):
    def is_active(self, request: Optional[WSGIRequest]) -> bool: ...
    def get_cleansed_multivaluedict(
        self, request: WSGIRequest, multivaluedict: QueryDict
    ) -> QueryDict: ...
    def get_post_parameters(
        self, request: Optional[WSGIRequest]
    ) -> Dict[Any, Any]: ...
    def cleanse_special_types(
        self,
        request: Optional[WSGIRequest],
        value: Optional[
            Union[
                Callable,
                Dict[
                    str,
                    Optional[Union[List[Enclosure], List[str], datetime, str]],
                ],
                Dict[str, Optional[Union[bool, TemplateResponseMixin]]],
                Dict[
                    str, Union[Tuple[int, int], BytesIO, FakePayload, int, str]
                ],
                Dict[str, Union[Tuple[str, Dict[str, bytes]], date]],
                Dict[
                    str,
                    Union[
                        django.db.backends.base.DatabaseWrapper, CursorWrapper
                    ],
                ],
                Dict[str, bytes],
                Dict[str, Model],
                Dict[str, BlockNode],
                Exception,
                List[Callable],
                List[Union[Dict[str, Union[bool, str]], ChangeList]],
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
                bytes,
                date,
                ModelAdmin,
                ChangeList,
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
                RequestFactory,
                ResolverMatch,
                URLResolver,
                Rss201rev2Feed,
                cached_property,
                SimplerXMLGenerator,
                ExceptionReporter,
                TemplateResponseMixin,
                int,
                str,
            ]
        ],
    ) -> Optional[
        Union[
            Callable,
            Dict[
                str, Optional[Union[List[Enclosure], List[str], datetime, str]]
            ],
            Dict[str, Optional[Union[bool, TemplateResponseMixin]]],
            Dict[str, Union[Tuple[int, int], BytesIO, FakePayload, int, str]],
            Dict[str, Union[Tuple[str, Dict[str, bytes]], date]],
            Dict[
                str,
                Union[django.db.backends.base.DatabaseWrapper, CursorWrapper],
            ],
            Dict[str, bytes],
            Dict[str, Model],
            Dict[str, BlockNode],
            Exception,
            List[Callable],
            List[Union[Dict[str, Union[bool, str]], ChangeList]],
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
            bytes,
            date,
            ModelAdmin,
            ChangeList,
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
            RequestFactory,
            ResolverMatch,
            URLResolver,
            Rss201rev2Feed,
            cached_property,
            SimplerXMLGenerator,
            ExceptionReporter,
            TemplateResponseMixin,
            int,
            str,
        ]
    ]: ...
    def get_traceback_frame_variables(self, request: Any, tb_frame: Any): ...

class ExceptionReporter:
    request: Optional[django.core.handlers.wsgi.WSGIRequest] = ...
    filter: django.views.debug.SafeExceptionReporterFilter = ...
    exc_type: None = ...
    exc_value: Optional[str] = ...
    tb: None = ...
    is_email: bool = ...
    template_info: None = ...
    template_does_not_exist: bool = ...
    postmortem: None = ...
    def __init__(
        self,
        request: Optional[WSGIRequest],
        exc_type: None,
        exc_value: Optional[str],
        tb: None,
        is_email: bool = ...,
    ) -> None: ...
    def get_traceback_data(
        self
    ) -> Dict[
        str,
        Optional[
            Union[
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[Any, Any],
                            Dict[
                                str,
                                Dict[
                                    str,
                                    Optional[
                                        Union[
                                            Dict[Any, Any],
                                            Dict[str, None],
                                            int,
                                            str,
                                        ]
                                    ],
                                ],
                            ],
                            Dict[str, Dict[str, str]],
                            Dict[str, None],
                            Dict[
                                str,
                                Union[
                                    Dict[str, Dict[str, str]],
                                    Dict[
                                        str,
                                        Union[
                                            Dict[
                                                str, Union[List[str], bool, str]
                                            ],
                                            Dict[str, Union[List[str], str]],
                                        ],
                                    ],
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, Union[List[str], str]],
                                            Dict[str, str],
                                        ],
                                    ],
                                    int,
                                ],
                            ],
                            List[Any],
                            List[
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, List[str]],
                                        List[str],
                                        bool,
                                        str,
                                    ],
                                ]
                            ],
                            List[Tuple[str, str]],
                            List[str],
                            int,
                            str,
                        ]
                    ],
                ],
                List[str],
                bool,
                datetime,
                str,
            ]
        ],
    ]: ...
    def get_traceback_html(self) -> SafeText: ...
    def get_traceback_text(self) -> SafeText: ...
    def get_traceback_frames(self) -> List[Any]: ...

def technical_404_response(
    request: WSGIRequest, exception: Http404
) -> HttpResponse: ...
def default_urlconf(request: WSGIRequest) -> HttpResponse: ...
