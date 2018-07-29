from collections import OrderedDict
from django.template.backends.base import BaseEngine
from django.template.backends.django import DjangoTemplates
from django.template.backends.dummy import TemplateStrings
from typing import (
    List,
    Tuple,
    Union,
)


def get_app_template_dirs(dirname: str) -> Tuple: ...


class EngineHandler:
    def __getitem__(self, alias: str) -> BaseEngine: ...
    def __iter__(self): ...
    def all(
        self
    ) -> Union[List[BaseEngine], List[TemplateStrings], List[DjangoTemplates]]: ...
    @cached_property
    def templates(self) -> OrderedDict: ...