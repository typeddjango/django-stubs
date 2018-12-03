from datetime import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from jinja2.environment import Template
from jinja2.exceptions import TemplateSyntaxError

from django.http.request import HttpRequest
from django.views.generic.base import TemplateView

from .base import BaseEngine

class Jinja2(BaseEngine):
    app_dirs: bool
    dirs: List[str]
    name: str
    template_context_processors: List[Callable]
    template_dirs: Tuple[str]
    app_dirname: str = ...
    context_processors: List[str] = ...
    env: jinja2.environment.Environment = ...
    def __init__(self, params: Dict[str, Union[Dict[str, Union[List[str], bool]], List[str], bool, str]]) -> None: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...
    def template_context_processors(self) -> List[Callable]: ...

class Template:
    template: jinja2.environment.Template = ...
    backend: django.template.backends.jinja2.Jinja2 = ...
    origin: django.template.backends.jinja2.Origin = ...
    def __init__(self, template: Template, backend: Jinja2) -> None: ...
    def render(
        self,
        context: Optional[
            Union[
                Dict[str, Dict[str, Optional[Union[Dict[str, bool], bool, str]]]],
                Dict[
                    str,
                    Dict[
                        str,
                        Optional[Union[Dict[str, str], List[Dict[str, Optional[Union[Dict[str, str], bool, str]]]], bool, str]],
                    ],
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, int],
                            List[Tuple[Optional[str], List[Dict[str, Union[Dict[str, bool], bool, str]]], int]],
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
                            List[
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, str],
                                        List[Tuple[None, List[Dict[str, Union[Dict[str, bool], bool, str]]], int]],
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
                ],
                Dict[
                    str,
                    Dict[
                        str,
                        Union[
                            Dict[str, str],
                            List[Tuple[Optional[str], List[Dict[str, Union[Dict[str, Union[bool, str]], time, int, str]]], int]],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                ],
                Dict[str, TemplateView],
                Dict[str, str],
            ]
        ] = ...,
        request: Optional[HttpRequest] = ...,
    ) -> str: ...

class Origin:
    name: str = ...
    template_name: Optional[str] = ...
    def __init__(self, name: str, template_name: Optional[str]) -> None: ...

def get_exception_info(exception: TemplateSyntaxError) -> Dict[str, Union[List[Tuple[int, str]], int, str]]: ...
