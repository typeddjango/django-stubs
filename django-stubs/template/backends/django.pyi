from datetime import datetime, time
from decimal import Decimal
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Union)
from unittest.mock import MagicMock

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.requests import RequestSite
from django.core.paginator import Page, Paginator
from django.db.models.base import Model
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.http.request import HttpRequest
from django.template.base import Origin, Template
from django.template.context import Context
from django.template.exceptions import TemplateDoesNotExist
from django.utils.safestring import SafeText
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView

from .base import BaseEngine


class DjangoTemplates(BaseEngine):
    app_dirs: bool
    dirs: List[str]
    name: str
    app_dirname: str = ...
    engine: django.template.engine.Engine = ...
    def __init__(
        self,
        params: Union[
            Dict[str, Union[Dict[str, Dict[str, str]], List[Any], bool, str]],
            Dict[
                str,
                Union[
                    Dict[str, List[Tuple[str, Dict[str, str]]]],
                    List[Any],
                    bool,
                    str,
                ],
            ],
            Dict[str, Union[Dict[str, List[str]], List[str], bool, str]],
            Dict[str, Union[Dict[str, Tuple[str]], List[str], bool, str]],
            Dict[str, Union[Dict[str, bool], List[Any], bool, str]],
            Dict[str, Union[Dict[str, str], List[Any], bool, str]],
        ],
    ) -> None: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...
    def get_templatetag_libraries(
        self, custom_libraries: Dict[str, str]
    ) -> Dict[str, str]: ...

class Template:
    template: django.template.base.Template = ...
    backend: django.template.backends.django.DjangoTemplates = ...
    def __init__(
        self, template: Template, backend: DjangoTemplates
    ) -> None: ...
    @property
    def origin(self) -> Origin: ...
    def render(
        self,
        context: Optional[
            Union[
                Dict[str, Any],
                Dict[
                    str,
                    Dict[
                        str,
                        Optional[
                            Union[Dict[str, Union[bool, float, str]], bool, str]
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Optional[
                            Union[
                                Dict[str, Union[Decimal, int, str]],
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Optional[
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    List[
                                                        Dict[
                                                            str,
                                                            Optional[
                                                                Union[
                                                                    Dict[
                                                                        str,
                                                                        Union[
                                                                            bool,
                                                                            str,
                                                                        ],
                                                                    ],
                                                                    bool,
                                                                    str,
                                                                ]
                                                            ],
                                                        ]
                                                    ],
                                                    bool,
                                                    str,
                                                ]
                                            ],
                                        ],
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                List[
                                                    Tuple[
                                                        None,
                                                        List[
                                                            Dict[
                                                                str,
                                                                Union[
                                                                    Dict[
                                                                        Any, Any
                                                                    ],
                                                                    bool,
                                                                    str,
                                                                ],
                                                            ]
                                                        ],
                                                        int,
                                                    ]
                                                ],
                                                bool,
                                                str,
                                            ],
                                        ],
                                    ]
                                ],
                                bool,
                                str,
                            ]
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[
                                Tuple[
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                    int,
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[
                                Union[
                                    Dict[
                                        str,
                                        Union[
                                            Dict[Any, Any],
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[Any, Any],
                                                        bool,
                                                        str,
                                                    ],
                                                ]
                                            ],
                                            bool,
                                            str,
                                        ],
                                    ],
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, bool],
                                            List[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[str, bool],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ]
                                            ],
                                            List[str],
                                            bool,
                                            str,
                                        ],
                                    ],
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[
                                Union[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        str,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, bool], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[
                                Union[
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, Union[bool, str]],
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[
                                                            str,
                                                            Union[bool, str],
                                                        ],
                                                        bool,
                                                        str,
                                                    ],
                                                ]
                                            ],
                                            bool,
                                            str,
                                        ],
                                    ],
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, Union[bool, str]],
                                            List[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[str, bool],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ]
                                            ],
                                            List[str],
                                            bool,
                                            str,
                                        ],
                                    ],
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[
                                Union[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, bool], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        str,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[int, str]],
                            List[
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, Union[bool, str]], bool, str
                                    ],
                                ]
                            ],
                            int,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[int, str]],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[Any, Any], time, int, str
                                            ],
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[int, str]],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, bool],
                                                Set[str],
                                                int,
                                                str,
                                            ],
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, bool],
                            List[
                                Tuple[
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
                                        ]
                                    ],
                                    int,
                                    int,
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, str],
                            List[Dict[str, Union[Dict[str, str], bool, str]]],
                            List[int],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, str],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str, Union[Dict[str, str], int, str]
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, str],
                            List[
                                Union[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, str], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        str,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    bool,
                                                    str,
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[
                    str, Optional[Union[List[Dict[str, str]], bool, ListView]]
                ],
                Dict[str, Optional[str]],
                Dict[str, Union[Callable, int]],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Optional[
                                Union[
                                    Dict[Any, Any],
                                    List[
                                        Dict[
                                            str,
                                            Optional[
                                                Union[Dict[Any, Any], bool, str]
                                            ],
                                        ]
                                    ],
                                    bool,
                                    str,
                                ]
                            ],
                        ],
                        List[Dict[str, Optional[Union[datetime, Model, str]]]],
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Optional[
                                Union[
                                    Dict[str, Union[bool, str]],
                                    List[
                                        Dict[
                                            str,
                                            Optional[
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    bool,
                                                    str,
                                                ]
                                            ],
                                        ]
                                    ],
                                    bool,
                                    str,
                                ]
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Optional[
                                Union[
                                    Dict[str, Union[bool, str]],
                                    List[
                                        Dict[
                                            str,
                                            Optional[
                                                Union[Dict[str, str], bool, str]
                                            ],
                                        ]
                                    ],
                                    int,
                                    str,
                                ]
                            ],
                        ],
                        TemplateResponseMixin,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Optional[
                                Union[
                                    Dict[str, str],
                                    List[
                                        Dict[
                                            str,
                                            Optional[
                                                Union[Dict[str, str], bool, str]
                                            ],
                                        ]
                                    ],
                                    bool,
                                    str,
                                ]
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[str, Optional[Union[Dict[str, str], bool, str]]],
                        List[Dict[str, str]],
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[Any, Any],
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Dict[Any, Any],
                                            List[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[str, bool],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ]
                                            ],
                                            List[str],
                                            bool,
                                            str,
                                        ],
                                    ]
                                ],
                                List[str],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[Any, Any],
                                List[
                                    Dict[str, Union[Dict[str, str], bool, str]]
                                ],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[bool, str]],
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, Union[bool, str]],
                                            bool,
                                            str,
                                        ],
                                    ]
                                ],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[bool, str]],
                                List[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    int,
                                                    str,
                                                ],
                                            ]
                                        ],
                                        int,
                                    ]
                                ],
                                List[str],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, str],
                                List[
                                    Dict[str, Union[Dict[str, str], bool, str]]
                                ],
                                List[str],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, str],
                                List[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, str], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ]
                                ],
                                bool,
                                str,
                            ],
                        ],
                        str,
                    ],
                ],
                Dict[
                    str,
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, str],
                                List[
                                    Union[
                                        Tuple[
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[str, str],
                                                        bool,
                                                        str,
                                                    ],
                                                ]
                                            ],
                                            int,
                                            int,
                                        ],
                                        Tuple[
                                            str,
                                            List[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[
                                                            str,
                                                            Union[bool, str],
                                                        ],
                                                        bool,
                                                        str,
                                                    ],
                                                ]
                                            ],
                                            int,
                                        ],
                                    ]
                                ],
                                List[str],
                                bool,
                                str,
                            ],
                        ],
                        List[Dict[str, str]],
                    ],
                ],
                Dict[
                    str,
                    Union[
                        List[Dict[str, str]], bool, Page, Paginator, ListView
                    ],
                ],
                Dict[str, Union[List[str], str]],
                Dict[str, Union[bool, str]],
                Dict[
                    str, Union[AuthenticationForm, LoginView, RequestSite, str]
                ],
                Dict[str, Union[Model, BaseForm, TemplateResponseMixin, str]],
                Dict[str, Union[Manager, QuerySet]],
                Dict[str, Template],
                Context,
                MagicMock,
            ]
        ] = ...,
        request: Optional[HttpRequest] = ...,
    ) -> SafeText: ...

def copy_exception(
    exc: TemplateDoesNotExist, backend: Optional[DjangoTemplates] = ...
) -> TemplateDoesNotExist: ...
def reraise(exc: TemplateDoesNotExist, backend: DjangoTemplates) -> Any: ...
def get_installed_libraries() -> Dict[str, str]: ...
def get_package_libraries(pkg: Any) -> Iterator[str]: ...
