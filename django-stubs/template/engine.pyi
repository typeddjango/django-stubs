from datetime import date, time, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from django.template.base import Origin, Template
from django.template.library import Library
from django.template.loaders.base import Loader
from django.utils.safestring import SafeText

from .base import Context, Template
from .context import _builtin_context_processors
from .exceptions import TemplateDoesNotExist
from .library import import_library


class Engine:
    template_context_processors: Tuple[Callable]
    template_loaders: List[django.template.loaders.base.Loader]
    default_builtins: Any = ...
    dirs: List[str] = ...
    app_dirs: bool = ...
    autoescape: bool = ...
    context_processors: Union[List[str], Tuple[str]] = ...
    debug: bool = ...
    loaders: Union[
        List[List[Union[Dict[str, str], str]]],
        List[
            Union[
                Tuple[
                    str,
                    Union[
                        Dict[str, str],
                        List[Any],
                        List[Tuple[str, Dict[str, str]]],
                        List[str],
                    ],
                ],
                str,
            ]
        ],
    ] = ...
    string_if_invalid: str = ...
    file_charset: str = ...
    libraries: Dict[str, str] = ...
    template_libraries: Dict[str, django.template.library.Library] = ...
    builtins: List[str] = ...
    template_builtins: List[django.template.library.Library] = ...
    def __init__(
        self,
        dirs: Optional[List[str]] = ...,
        app_dirs: bool = ...,
        context_processors: Optional[Union[List[str], Tuple[str]]] = ...,
        debug: bool = ...,
        loaders: Optional[
            Union[
                List[List[Union[Dict[str, str], str]]],
                List[
                    Union[
                        Tuple[
                            str,
                            Union[
                                Dict[str, str],
                                List[Any],
                                List[Tuple[str, Dict[str, str]]],
                                List[str],
                            ],
                        ],
                        str,
                    ]
                ],
            ]
        ] = ...,
        string_if_invalid: str = ...,
        file_charset: str = ...,
        libraries: Optional[Dict[str, str]] = ...,
        builtins: Optional[List[str]] = ...,
        autoescape: bool = ...,
    ) -> None: ...
    @staticmethod
    def get_default() -> Engine: ...
    def template_context_processors(self) -> Tuple[Callable]: ...
    def get_template_builtins(self, builtins: List[str]) -> List[Library]: ...
    def get_template_libraries(
        self, libraries: Dict[str, str]
    ) -> Dict[str, Library]: ...
    def template_loaders(self) -> List[Loader]: ...
    def get_template_loaders(
        self,
        template_loaders: Union[
            List[List[Union[Dict[str, str], str]]],
            List[
                Union[
                    Tuple[
                        str,
                        Union[
                            Dict[str, str],
                            List[Any],
                            List[Tuple[str, Dict[str, str]]],
                            List[str],
                        ],
                    ],
                    str,
                ]
            ],
        ],
    ) -> List[Loader]: ...
    def find_template_loader(
        self,
        loader: Union[
            List[Union[Dict[str, str], str]],
            Tuple[
                str,
                Union[
                    Dict[str, str], List[Tuple[str, Dict[str, str]]], List[str]
                ],
            ],
            str,
        ],
    ) -> Loader: ...
    def find_template(
        self, name: str, dirs: None = ..., skip: Optional[List[Origin]] = ...
    ) -> Tuple[Template, Origin]: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...
    def render_to_string(
        self,
        template_name: str,
        context: Optional[
            Union[
                Dict[str, Callable],
                Dict[str, Dict[Union[int, str], str]],
                Dict[str, Dict[str, Callable]],
                Dict[str, Dict[str, Dict[str, str]]],
                Dict[str, Dict[str, List[Tuple[str, int]]]],
                Dict[str, Dict[str, Tuple[str, str, str, str]]],
                Dict[str, List[Dict[str, Union[List[int], int]]]],
                Dict[str, List[Dict[str, Union[List[str], str]]]],
                Dict[str, List[Dict[str, Union[int, str]]]],
                Dict[str, List[Dict[str, date]]],
                Dict[str, List[List[Tuple[int, str]]]],
                Dict[str, List[Template]],
                Dict[str, Optional[int]],
                Dict[str, Optional[str]],
                Dict[
                    str, Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]
                ],
                Dict[
                    str,
                    Tuple[
                        Tuple[str, Union[int, str]], Tuple[str, Union[int, str]]
                    ],
                ],
                Dict[str, Tuple[int, int]],
                Dict[str, Tuple[str, str]],
                Dict[str, Union[Dict[str, int], List[Union[List[str], str]]]],
                Dict[str, Union[Dict[str, int], str]],
                Dict[
                    str,
                    Union[List[Optional[Union[Dict[Any, Any], int, str]]], int],
                ],
                Dict[str, Union[List[Union[List[SafeText], str]], str]],
                Dict[str, Union[List[int], str]],
                Dict[str, Union[date, timedelta]],
                Dict[str, Union[float, int]],
                Dict[str, Union[int, str]],
                Dict[str, time],
                Dict[str, Template],
                Dict[str, range],
            ]
        ] = ...,
    ) -> SafeText: ...
    def select_template(self, template_name_list: List[str]) -> Template: ...
