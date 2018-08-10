from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from unittest.mock import MagicMock

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.requests import RequestSite
from django.core.paginator import Page, Paginator
from django.db.models.base import Model
from django.forms.forms import BaseForm
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.template.backends.django import Template
from django.template.backends.jinja2 import Template
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .loader import get_template, select_template


class ContentNotRenderedError(Exception): ...

class SimpleTemplateResponse(HttpResponse):
    closed: bool
    cookies: http.cookies.SimpleCookie
    status_code: int
    rendering_attrs: Any = ...
    template_name: Union[
        List[str], django.template.backends.django.Template, str
    ] = ...
    context_data: Optional[
        Union[Dict[str, Union[Callable, int]], Dict[str, str]]
    ] = ...
    using: Optional[str] = ...
    def __init__(
        self,
        template: Union[List[str], Template, str],
        context: Optional[
            Union[
                Dict[str, Any],
                Dict[str, List[Dict[str, Any]]],
                Dict[
                    str,
                    Optional[
                        Union[
                            List[
                                Dict[str, Optional[Union[datetime, Model, str]]]
                            ],
                            bool,
                            ListView,
                        ]
                    ],
                ],
                Dict[str, Union[Callable, int]],
                Dict[str, Union[Dict[str, str], DetailView]],
                Dict[
                    str,
                    Union[
                        List[Dict[str, str]], bool, Page, Paginator, ListView
                    ],
                ],
                Dict[str, Union[List[str], str]],
                Dict[
                    str, Union[AuthenticationForm, LoginView, RequestSite, str]
                ],
                Dict[str, Union[Model, BaseForm, TemplateResponseMixin, str]],
                MagicMock,
            ]
        ] = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: Optional[str] = ...,
        using: Optional[str] = ...,
    ) -> None: ...
    def resolve_template(
        self, template: Union[List[str], Template, str]
    ) -> Union[Template, Template]: ...
    def resolve_context(
        self,
        context: Optional[
            Union[
                Dict[str, Any],
                Dict[str, List[Dict[str, Any]]],
                Dict[
                    str,
                    Optional[
                        Union[
                            List[
                                Dict[str, Optional[Union[datetime, Model, str]]]
                            ],
                            bool,
                            ListView,
                        ]
                    ],
                ],
                Dict[str, Union[Callable, int]],
                Dict[str, Union[Dict[str, str], DetailView]],
                Dict[
                    str,
                    Union[
                        List[Dict[str, str]], bool, Page, Paginator, ListView
                    ],
                ],
                Dict[str, Union[List[str], str]],
                Dict[
                    str, Union[AuthenticationForm, LoginView, RequestSite, str]
                ],
                Dict[str, Union[Model, BaseForm, TemplateResponseMixin, str]],
                MagicMock,
            ]
        ],
    ) -> Optional[
        Union[
            Dict[str, Any],
            Dict[str, List[Dict[str, Any]]],
            Dict[
                str,
                Optional[
                    Union[
                        List[Dict[str, Optional[Union[datetime, Model, str]]]],
                        bool,
                        ListView,
                    ]
                ],
            ],
            Dict[str, Union[Callable, int]],
            Dict[str, Union[Dict[str, str], DetailView]],
            Dict[
                str,
                Union[List[Dict[str, str]], bool, Page, Paginator, ListView],
            ],
            Dict[str, Union[List[str], str]],
            Dict[str, Union[AuthenticationForm, LoginView, RequestSite, str]],
            Dict[str, Union[Model, BaseForm, TemplateResponseMixin, str]],
            MagicMock,
        ]
    ]: ...
    @property
    def rendered_content(self) -> str: ...
    def add_post_render_callback(self, callback: Callable) -> None: ...
    content: Any = ...
    def render(self) -> SimpleTemplateResponse: ...
    @property
    def is_rendered(self) -> bool: ...
    def __iter__(self) -> Any: ...
    @property
    def content(self): ...
    @content.setter
    def content(self, value: Any) -> None: ...

class TemplateResponse(SimpleTemplateResponse):
    client: django.test.client.Client
    closed: bool
    context: django.template.context.RequestContext
    context_data: Optional[
        Union[
            Dict[str, Any],
            Dict[str, List[Dict[str, Any]]],
            Dict[
                str,
                Optional[
                    Union[
                        List[
                            Dict[
                                str,
                                Optional[
                                    Union[
                                        datetime.datetime,
                                        django.db.models.base.Model,
                                        str,
                                    ]
                                ],
                            ]
                        ],
                        bool,
                        django.views.generic.list.ListView,
                    ]
                ],
            ],
            Dict[str, Union[Callable, int]],
            Dict[
                str,
                Union[Dict[str, str], django.views.generic.detail.DetailView],
            ],
            Dict[
                str,
                Union[
                    List[Dict[str, str]],
                    bool,
                    django.core.paginator.Page,
                    django.core.paginator.Paginator,
                    django.views.generic.list.ListView,
                ],
            ],
            Dict[str, Union[List[str], str]],
            Dict[
                str,
                Union[
                    django.contrib.auth.forms.AuthenticationForm,
                    django.contrib.auth.views.LoginView,
                    django.contrib.sites.requests.RequestSite,
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    django.db.models.base.Model,
                    django.forms.forms.BaseForm,
                    django.views.generic.base.TemplateResponseMixin,
                    str,
                ],
            ],
            unittest.mock.MagicMock,
        ]
    ]
    cookies: http.cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, Union[django.test.client.FakePayload, int, str]]
    resolver_match: django.utils.functional.SimpleLazyObject
    status_code: int
    template_name: Union[
        List[str], django.template.backends.django.Template, str
    ]
    templates: List[django.template.base.Template]
    using: Optional[str]
    wsgi_request: django.core.handlers.wsgi.WSGIRequest
    rendering_attrs: Any = ...
    def __init__(
        self,
        request: HttpRequest,
        template: Union[List[str], Template, str],
        context: Optional[
            Union[
                Dict[str, Any],
                Dict[str, List[Dict[str, Any]]],
                Dict[
                    str,
                    Optional[
                        Union[
                            List[
                                Dict[str, Optional[Union[datetime, Model, str]]]
                            ],
                            bool,
                            ListView,
                        ]
                    ],
                ],
                Dict[str, Union[Callable, int]],
                Dict[str, Union[Dict[str, str], DetailView]],
                Dict[
                    str,
                    Union[
                        List[Dict[str, str]], bool, Page, Paginator, ListView
                    ],
                ],
                Dict[str, Union[List[str], str]],
                Dict[
                    str, Union[AuthenticationForm, LoginView, RequestSite, str]
                ],
                Dict[str, Union[Model, BaseForm, TemplateResponseMixin, str]],
                MagicMock,
            ]
        ] = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: None = ...,
        using: Optional[str] = ...,
    ) -> None: ...
