from datetime import time
from typing import Any, Dict, List, Optional, Tuple, Union

from django.template.backends.base import BaseEngine
from django.template.backends.django import Template
from django.template.backends.jinja2 import Template

ROOT: Any

def get_default_renderer() -> DjangoTemplates: ...

class BaseRenderer:
    def get_template(self, template_name: str) -> Any: ...
    def render(
        self,
        template_name: str,
        context: Dict[
            str,
            Union[
                Dict[
                    str, Optional[Union[Dict[str, bool], List[Dict[str, Optional[Union[Dict[str, str], bool, str]]]], bool, str]]
                ],
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Dict[
                                str,
                                Union[
                                    Dict[str, Union[bool, str]],
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
                Dict[
                    str,
                    Union[
                        Dict[str, Union[int, str]],
                        List[Tuple[Optional[str], List[Dict[str, Union[Dict[str, Union[bool, str]], time, int, str]]], int]],
                        List[str],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, str], List[Dict[str, Union[Dict[str, str], bool, str]]], List[int], bool, str]],
            ],
        ],
        request: None = ...,
    ) -> str: ...

class EngineMixin:
    def get_template(self, template_name: str) -> Union[Template, Template]: ...
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    engine: django.template.backends.django.DjangoTemplates
    backend: Any = ...

class Jinja2(EngineMixin, BaseRenderer):
    engine: django.template.backends.jinja2.Jinja2
    backend: Any = ...

class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template: ...
