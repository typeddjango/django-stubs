from datetime import date, time, timedelta
from decimal import Decimal
from enum import Enum
from io import BytesIO
from sqlite3 import OperationalError
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Type, Union)
from uuid import UUID

from django.contrib.admin.filters import FieldListFilter
from django.contrib.admin.helpers import (AdminForm, Fieldline, Fieldset,
                                          InlineAdminFormSet)
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.context_processors import PermLookupDict, PermWrapper
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.base import BaseStorage, Message
from django.core.exceptions import FieldDoesNotExist
from django.core.files.base import File
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.fields import AutoField
from django.db.models.fields.files import FieldFile
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.forms.boundfield import BoundField, BoundWidget
from django.forms.forms import BaseForm
from django.forms.utils import ErrorDict
from django.forms.widgets import Media
from django.template.backends.django import Template
from django.template.backends.dummy import TemplateStrings
from django.template.context import Context
from django.template.defaulttags import GroupedResult
from django.template.engine import Engine
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.template.library import Library
from django.template.loaders.base import Loader
from django.test.client import FakePayload
from django.urls.resolvers import (CheckURLMixin, LocalePrefixPattern,
                                   URLPattern, URLResolver)
from django.utils.safestring import SafeText
from django.utils.timezone import FixedOffset
from django.views.debug import CallableSettingWrapper

from .exceptions import TemplateSyntaxError

FILTER_SEPARATOR: str
FILTER_ARGUMENT_SEPARATOR: str
VARIABLE_ATTRIBUTE_SEPARATOR: str
BLOCK_TAG_START: str
BLOCK_TAG_END: str
VARIABLE_TAG_START: str
VARIABLE_TAG_END: str
COMMENT_TAG_START: str
COMMENT_TAG_END: str
TRANSLATOR_COMMENT_MARK: str
SINGLE_BRACE_START: str
SINGLE_BRACE_END: str
UNKNOWN_SOURCE: str
tag_re: Any
logger: Any

class TokenType(Enum):
    TEXT: int = ...
    VAR: int = ...
    BLOCK: int = ...
    COMMENT: int = ...

class VariableDoesNotExist(Exception):
    msg: str = ...
    params: Union[
        Tuple[Dict[str, str]],
        Tuple[
            str,
            Optional[
                Union[
                    Dict[str, Union[int, str]],
                    List[str],
                    django.contrib.admin.views.main.ChangeList,
                    django.template.context.Context,
                    django.urls.resolvers.URLResolver,
                    int,
                    str,
                ]
            ],
        ],
    ] = ...
    def __init__(
        self,
        msg: str,
        params: Union[
            Tuple[Dict[str, str]],
            Tuple[
                str,
                Optional[
                    Union[
                        Dict[str, Union[int, str]],
                        List[str],
                        ChangeList,
                        Context,
                        URLResolver,
                        int,
                        str,
                    ]
                ],
            ],
        ] = ...,
    ) -> None: ...

class Origin:
    name: str = ...
    template_name: Optional[Union[bytes, str]] = ...
    loader: Optional[
        Union[
            django.template.backends.dummy.TemplateStrings,
            django.template.loaders.base.Loader,
        ]
    ] = ...
    def __init__(
        self,
        name: str,
        template_name: Optional[Union[bytes, str]] = ...,
        loader: Optional[Union[TemplateStrings, Loader]] = ...,
    ) -> None: ...
    def __eq__(self, other: Origin) -> bool: ...
    @property
    def loader_name(self) -> Optional[str]: ...

class Template:
    name: Optional[str] = ...
    origin: django.template.base.Origin = ...
    engine: django.template.engine.Engine = ...
    source: str = ...
    nodelist: django.template.base.NodeList = ...
    def __init__(
        self,
        template_string: str,
        origin: Optional[Origin] = ...,
        name: Optional[str] = ...,
        engine: Optional[Engine] = ...,
    ) -> None: ...
    def __iter__(self) -> None: ...
    def render(self, context: Context) -> Any: ...
    def compile_nodelist(self) -> NodeList: ...
    def get_exception_info(
        self, exception: Exception, token: Token
    ) -> Dict[str, Union[List[Tuple[int, SafeText]], int, str]]: ...

def linebreak_iter(template_source: str) -> Iterator[int]: ...

class Token:
    contents: str
    token_type: django.template.base.TokenType
    lineno: Optional[int] = ...
    position: Optional[Tuple[int, int]] = ...
    def __init__(
        self,
        token_type: TokenType,
        contents: str,
        position: Optional[Tuple[int, int]] = ...,
        lineno: Optional[int] = ...,
    ) -> None: ...
    def split_contents(self) -> List[str]: ...

class Lexer:
    template_string: str = ...
    verbatim: Union[bool, str] = ...
    def __init__(self, template_string: str) -> None: ...
    def tokenize(self) -> List[Token]: ...
    def create_token(
        self,
        token_string: str,
        position: Optional[Tuple[int, int]],
        lineno: int,
        in_tag: bool,
    ) -> Token: ...

class DebugLexer(Lexer):
    template_string: str
    verbatim: Union[bool, str]
    def tokenize(self) -> List[Token]: ...

class Parser:
    tokens: Union[List[django.template.base.Token], str] = ...
    tags: Dict[str, Callable] = ...
    filters: Dict[str, Callable] = ...
    command_stack: List[Tuple[str, django.template.base.Token]] = ...
    libraries: Dict[str, django.template.library.Library] = ...
    origin: Optional[django.template.base.Origin] = ...
    def __init__(
        self,
        tokens: Union[List[Token], str],
        libraries: Optional[Dict[str, Library]] = ...,
        builtins: Optional[List[Library]] = ...,
        origin: Optional[Origin] = ...,
    ) -> None: ...
    def parse(self, parse_until: Optional[Tuple[str]] = ...) -> NodeList: ...
    def skip_past(self, endtag: str) -> None: ...
    def extend_nodelist(
        self, nodelist: NodeList, node: Node, token: Token
    ) -> None: ...
    def error(
        self, token: Token, e: Union[RuntimeError, TemplateSyntaxError, str]
    ) -> Union[RuntimeError, TemplateSyntaxError]: ...
    def invalid_block_tag(
        self,
        token: Token,
        command: str,
        parse_until: Union[List[Any], Tuple[str]] = ...,
    ) -> Any: ...
    def unclosed_block_tag(self, parse_until: Tuple[str]) -> Any: ...
    def next_token(self) -> Token: ...
    def prepend_token(self, token: Token) -> None: ...
    def delete_first_token(self) -> None: ...
    def add_library(self, lib: Library) -> None: ...
    def compile_filter(self, token: str) -> FilterExpression: ...
    def find_filter(self, filter_name: str) -> Callable: ...

constant_string: Any
filter_raw_string: Any
filter_re: Any

class FilterExpression:
    token: str = ...
    filters: List[
        Tuple[
            Callable,
            Union[
                List[Any],
                List[Tuple[bool, django.template.base.Variable]],
                List[Tuple[bool, django.utils.safestring.SafeText]],
            ],
        ]
    ] = ...
    var: Union[
        django.template.base.Variable, django.utils.safestring.SafeText
    ] = ...
    def __init__(self, token: str, parser: Parser) -> None: ...
    def resolve(
        self,
        context: Union[Dict[str, Dict[str, str]], Context],
        ignore_failures: bool = ...,
    ) -> Optional[
        Union[
            AttributeError,
            Dict[str, Optional[Union[Dict[str, Union[bool, str]], bool, str]]],
            Dict[str, Union[Dict[str, Union[bool, str]], time, int, str]],
            Dict[str, Union[Dict[str, bool], Set[str], int, str]],
            Dict[str, Union[List[Tuple[int, SafeText]], int, str]],
            Dict[str, Union[List[int], int]],
            Iterator[Any],
            KeyError,
            List[Dict[str, Optional[Union[Dict[Any, Any], bool, str]]]],
            List[
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
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
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
                ]
            ],
            List[
                Dict[
                    str,
                    Union[
                        List[
                            Union[
                                Dict[str, Union[List[Any], str]],
                                Dict[
                                    str,
                                    Union[
                                        List[Dict[str, Union[List[Any], str]]],
                                        str,
                                    ],
                                ],
                            ]
                        ],
                        str,
                    ],
                ]
            ],
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
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[Any],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                    Dict[str, Union[Dict[str, str], bool, str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Optional[Union[Dict[str, str], int, str]]],
                    Dict[str, Union[List[int], int]],
                    Tuple[
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
                                                    str,
                                                    Union[List[str], bool, str],
                                                ],
                                                Dict[
                                                    str, Union[List[str], str]
                                                ],
                                            ],
                                        ],
                                        Dict[
                                            str,
                                            Union[
                                                Dict[
                                                    str, Union[List[str], str]
                                                ],
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
                                CallableSettingWrapper,
                                int,
                                str,
                            ]
                        ],
                        Optional[
                            Union[
                                Dict[Any, Any],
                                Dict[int, None],
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
                                                    str,
                                                    Union[List[str], bool, str],
                                                ],
                                                Dict[
                                                    str, Union[List[str], str]
                                                ],
                                            ],
                                        ],
                                        Dict[
                                            str,
                                            Union[
                                                Dict[
                                                    str, Union[List[str], str]
                                                ],
                                                Dict[str, str],
                                            ],
                                        ],
                                        int,
                                    ],
                                ],
                                Dict[str, Union[Dict[str, str], str]],
                                List[Any],
                                List[
                                    Dict[
                                        str,
                                        Union[
                                            Dict[
                                                str,
                                                List[
                                                    Tuple[str, Dict[str, str]]
                                                ],
                                            ],
                                            str,
                                        ],
                                    ]
                                ],
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
                                List[Dict[str, Union[List[Any], bool, str]]],
                                List[Dict[str, Union[List[str], str]]],
                                List[Tuple[str, str]],
                                List[str],
                                Tuple[int, int],
                                BytesIO,
                                FakePayload,
                                CallableSettingWrapper,
                                int,
                                str,
                            ]
                        ],
                    ],
                    FieldListFilter,
                ]
            ],
            List[
                Union[
                    Dict[str, Optional[Union[date, Model, str]]],
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
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
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
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
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ]
            ],
            List[
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[Dict[str, Union[Dict[Any, Any], bool, str]]],
                            bool,
                            str,
                        ],
                    ],
                    Dict[
                        str,
                        Union[
                            Dict[str, bool],
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
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                    List[Union[List[SafeText], str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[Dict[Any, Any], bool, time, str]],
                    Dict[str, Union[Dict[str, bool], Set[str], int, str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[List[Any], str]],
                    Dict[
                        str, Union[List[Dict[str, Union[List[Any], str]]], str]
                    ],
                ]
            ],
            List[Union[List[Tuple[int, str]], Tuple[int, int, int]]],
            List[Union[List[URLPattern], List[URLResolver]]],
            List[
                Union[
                    Tuple[
                        None,
                        List[Dict[str, Union[Dict[str, bool], bool, str]]],
                        int,
                    ],
                    Tuple[
                        str,
                        List[Dict[str, Union[Dict[Any, Any], bool, str]]],
                        int,
                    ],
                ]
            ],
            List[Union[Tuple[None, int, int], int]],
            List[Union[URLPattern, URLResolver]],
            List[InlineAdminFormSet],
            List[BoundField],
            List[GroupedResult],
            List[TemplateDoesNotExist],
            List[str],
            Set[Any],
            Tuple,
            TypeError,
            date,
            time,
            Decimal,
            FieldListFilter,
            AdminForm,
            Fieldline,
            Fieldset,
            InlineAdminFormSet,
            ChangeList,
            PermLookupDict,
            PermWrapper,
            AnonymousUser,
            BaseStorage,
            Message,
            FieldDoesNotExist,
            WSGIRequest,
            Model,
            AutoField,
            files.FieldFile,
            QuerySet,
            BoundField,
            BoundWidget,
            BaseForm,
            Media,
            Template,
            Template,
            CheckURLMixin,
            LocalePrefixPattern,
            FixedOffset,
            float,
            int,
            range,
            OperationalError,
            str,
            UUID,
        ]
    ]: ...
    def args_check(
        name: str,
        func: Callable,
        provided: List[Tuple[bool, Union[Variable, SafeText]]],
    ) -> bool: ...
    args_check: Any = ...

class Variable:
    var: Union[Dict[Any, Any], str] = ...
    literal: Optional[Union[django.utils.safestring.SafeText, float, int]] = ...
    lookups: Optional[Tuple[str]] = ...
    translate: bool = ...
    message_context: Optional[str] = ...
    def __init__(self, var: Union[Dict[Any, Any], str]) -> None: ...
    def resolve(
        self,
        context: Union[
            Dict[str, Dict[str, Union[int, str]]],
            Dict[str, Union[int, str]],
            Context,
            int,
            str,
        ],
    ) -> Optional[
        Union[
            AttributeError,
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
                        int,
                        str,
                    ]
                ],
            ],
            Dict[str, Union[Dict[Any, Any], bool, time, str]],
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
                    List[int],
                    int,
                ],
            ],
            Dict[str, Union[Dict[str, bool], Set[str], int, str]],
            Dict[str, Union[List[Tuple[int, SafeText]], int, str]],
            Iterator[Any],
            KeyError,
            List[
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[str, List[Tuple[str, Dict[str, str]]]],
                            bool,
                            str,
                        ]
                    ],
                ]
            ],
            List[
                Dict[
                    str,
                    Union[
                        Dict[str, List[str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
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
                ]
            ],
            List[
                Dict[
                    str,
                    Union[
                        List[
                            Union[
                                Dict[str, Union[List[Any], str]],
                                Dict[
                                    str,
                                    Union[
                                        List[Dict[str, Union[List[Any], str]]],
                                        str,
                                    ],
                                ],
                            ]
                        ],
                        str,
                    ],
                ]
            ],
            List[
                Optional[
                    Union[
                        Dict[str, Optional[Union[date, Model, str]]], int, str
                    ]
                ]
            ],
            List[
                Union[
                    Callable,
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[Dict[str, Union[Dict[Any, Any], bool, str]]],
                            bool,
                            str,
                        ],
                    ],
                    Dict[
                        str,
                        Union[
                            Dict[str, bool],
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
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ]
            ],
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
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[Any],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                    URLPattern,
                ]
            ],
            List[
                Union[
                    Dict[str, Optional[Union[Dict[str, str], int, str]]],
                    Dict[str, Union[List[int], int]],
                    Tuple[None, int, int],
                    FieldListFilter,
                ]
            ],
            List[
                Union[
                    Dict[str, Union[Dict[Any, Any], bool, time, str]],
                    Dict[str, Union[Dict[str, bool], Set[str], int, str]],
                ]
            ],
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
                                        Dict[str, Union[bool, str]], bool, str
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
                                ]
                            ],
                            List[str],
                            int,
                            str,
                        ],
                    ],
                    Tuple[Union[int, str], Union[int, str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[Dict[str, Union[bool, str]], bool, str]],
                    Dict[str, Union[Dict[str, str], bool, str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[List[Any], str]],
                    Dict[
                        str, Union[List[Dict[str, Union[List[Any], str]]], str]
                    ],
                ]
            ],
            List[
                Union[
                    List[Tuple[int, str]],
                    Tuple[
                        None,
                        List[Dict[str, Union[Dict[str, bool], bool, str]]],
                        int,
                    ],
                    Tuple[int, int, int],
                ]
            ],
            List[Union[List[Union[List[SafeText], str]], str]],
            List[Union[List[Union[List[str], str]], SafeText]],
            List[Union[List[URLPattern], List[URLResolver]]],
            List[
                Union[
                    Tuple[
                        None,
                        List[Dict[str, Union[Dict[str, bool], bool, str]]],
                        int,
                    ],
                    Tuple[
                        str,
                        List[Dict[str, Union[Dict[Any, Any], bool, str]]],
                        int,
                    ],
                ]
            ],
            List[InlineAdminFormSet],
            List[BoundField],
            List[GroupedResult],
            List[TemplateDoesNotExist],
            List[URLResolver],
            Set[Any],
            Tuple,
            TypeError,
            BytesIO,
            date,
            time,
            timedelta,
            Decimal,
            FieldListFilter,
            AdminForm,
            Fieldline,
            Fieldset,
            InlineAdminFormSet,
            ChangeList,
            PermLookupDict,
            PermWrapper,
            AnonymousUser,
            BaseStorage,
            Message,
            FieldDoesNotExist,
            File,
            WSGIRequest,
            Model,
            AutoField,
            Options,
            QuerySet,
            BoundField,
            BoundWidget,
            BaseForm,
            Media,
            Template,
            Template,
            FakePayload,
            CheckURLMixin,
            LocalePrefixPattern,
            FixedOffset,
            CallableSettingWrapper,
            float,
            int,
            range,
            OperationalError,
            str,
            UUID,
        ]
    ]: ...

class Node:
    must_be_first: bool = ...
    child_nodelists: Any = ...
    token: Any = ...
    def render(self, context: Any) -> None: ...
    def render_annotated(self, context: Context) -> Union[int, str]: ...
    def __iter__(self) -> None: ...
    def get_nodes_by_type(self, nodetype: Type[Node]) -> List[Node]: ...

class NodeList(list):
    contains_nontext: bool = ...
    def render(self, context: Context) -> SafeText: ...
    def get_nodes_by_type(self, nodetype: Type[Node]) -> List[Node]: ...

class TextNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    s: str = ...
    def __init__(self, s: str) -> None: ...
    def render(self, context: Context) -> str: ...

def render_value_in_context(
    value: Optional[
        Union[
            AttributeError,
            Dict[str, str],
            KeyError,
            List[ErrorDict],
            List[int],
            List[str],
            Tuple[int, int, int, int],
            TypeError,
            date,
            Decimal,
            AnonymousUser,
            Message,
            FieldDoesNotExist,
            Model,
            FieldFile,
            QuerySet,
            BoundField,
            BoundWidget,
            BaseForm,
            Media,
            CheckURLMixin,
            LocalePrefixPattern,
            float,
            int,
            str,
        ]
    ],
    context: Context,
) -> str: ...

class VariableNode(Node):
    origin: django.template.base.Origin
    token: django.template.base.Token
    filter_expression: django.template.base.FilterExpression = ...
    def __init__(self, filter_expression: FilterExpression) -> None: ...
    def render(self, context: Context) -> str: ...

kwarg_re: Any

def token_kwargs(
    bits: List[str], parser: Parser, support_legacy: bool = ...
) -> Dict[str, FilterExpression]: ...
