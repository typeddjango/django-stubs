from itertools import cycle
from typing import Any, Callable, Dict, Iterator, List, Optional, Type, Union

from django.contrib.admin.templatetags.admin_list import ResultList
from django.contrib.admin.views.main import ChangeList
from django.db.models.base import Model
from django.db.models.options import Options
from django.forms.boundfield import BoundField
from django.http.request import HttpRequest
from django.template.base import Node, Origin, Template
from django.template.defaulttags import CycleNode, IfChangedNode
from django.template.library import InclusionNode
from django.template.loader_tags import BlockContext


class ContextPopException(Exception): ...

class ContextDict(dict):
    context: django.template.context.BaseContext = ...
    def __init__(
        self, context: BaseContext, *args: Any, **kwargs: Any
    ) -> None: ...
    def __enter__(self) -> ContextDict: ...
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...

class BaseContext:
    def __init__(self, dict_: Any = ...) -> None: ...
    def __copy__(self) -> BaseContext: ...
    def __iter__(self) -> None: ...
    def push(self, *args: Any, **kwargs: Any) -> ContextDict: ...
    def pop(self) -> ContextDict: ...
    def __setitem__(self, key: Union[Node, str], value: Any) -> None: ...
    def set_upward(self, key: str, value: Union[int, str]) -> None: ...
    def __getitem__(self, key: Union[int, str]) -> Any: ...
    def __delitem__(self, key: Any) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def get(
        self, key: str, otherwise: Optional[int] = ...
    ) -> Optional[Union[Options, int, str]]: ...
    def setdefault(
        self,
        key: Union[IfChangedNode, str],
        default: Optional[Union[List[Origin], int]] = ...,
    ) -> Optional[Union[List[Origin], int]]: ...
    def new(
        self,
        values: Optional[
            Union[
                Dict[
                    str,
                    Union[
                        List[Dict[str, Union[int, str]]],
                        List[ResultList],
                        List[BoundField],
                        ChangeList,
                        int,
                    ],
                ],
                Dict[str, Union[List[Dict[str, str]], ChangeList, int, str]],
                Dict[str, Union[ChangeList, int, range, str]],
                Context,
            ]
        ] = ...,
    ) -> Context: ...
    def flatten(
        self
    ) -> Dict[
        str, Optional[Union[Dict[str, Union[Type[Any], str]], int, str]]
    ]: ...
    def __eq__(self, other: Context) -> bool: ...

class Context(BaseContext):
    dicts: Any
    autoescape: bool = ...
    use_l10n: Optional[bool] = ...
    use_tz: Optional[bool] = ...
    template_name: Optional[str] = ...
    render_context: django.template.context.RenderContext = ...
    template: Optional[django.template.base.Template] = ...
    def __init__(
        self,
        dict_: Any = ...,
        autoescape: bool = ...,
        use_l10n: Optional[bool] = ...,
        use_tz: None = ...,
    ) -> None: ...
    def bind_template(self, template: Template) -> Iterator[None]: ...
    def __copy__(self) -> Context: ...
    def update(
        self,
        other_dict: Union[
            Dict[str, Model], Dict[str, int], Dict[str, str], Context
        ],
    ) -> ContextDict: ...

class RenderContext(BaseContext):
    dicts: List[Dict[Union[django.template.loader_tags.IncludeNode, str], str]]
    template: Optional[django.template.base.Template] = ...
    def __iter__(self) -> None: ...
    def __contains__(self, key: Union[CycleNode, str]) -> bool: ...
    def get(
        self, key: Union[InclusionNode, str], otherwise: None = ...
    ) -> Optional[Union[Template, BlockContext]]: ...
    def __getitem__(
        self, key: Union[Node, str]
    ) -> Optional[Union[List[Origin], BlockContext, cycle]]: ...
    def push_state(
        self, template: Template, isolated_context: bool = ...
    ) -> Iterator[None]: ...

class RequestContext(Context):
    autoescape: bool
    dicts: List[Dict[str, str]]
    render_context: django.template.context.RenderContext
    template_name: Optional[str]
    use_l10n: None
    use_tz: None
    request: django.http.request.HttpRequest = ...
    def __init__(
        self,
        request: HttpRequest,
        dict_: Optional[
            Dict[str, Union[Dict[str, Union[Type[Any], str]], str]]
        ] = ...,
        processors: Optional[List[Callable]] = ...,
        use_l10n: None = ...,
        use_tz: None = ...,
        autoescape: bool = ...,
    ) -> None: ...
    template: Optional[django.template.base.Template] = ...
    def bind_template(self, template: Template) -> Iterator[None]: ...
    def new(
        self,
        values: Optional[
            Union[
                Dict[str, Union[Dict[str, str], List[Dict[str, str]], bool]],
                Dict[str, Union[List[Any], ChangeList, int, str]],
                Dict[
                    str,
                    Union[
                        List[Dict[str, Optional[Union[int, str]]]],
                        List[ResultList],
                        List[BoundField],
                        ChangeList,
                        int,
                    ],
                ],
                Dict[str, Union[ChangeList, int, range, str]],
                Context,
            ]
        ] = ...,
    ) -> RequestContext: ...

def make_context(
    context: Any, request: Optional[HttpRequest] = ..., **kwargs: Any
) -> Context: ...
