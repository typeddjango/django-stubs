from typing import Any, Mapping, Optional, Sequence, Union

from django.http.request import HttpRequest
from django.template.exceptions import TemplateDoesNotExist as TemplateDoesNotExist  # noqa: F401
from django.utils.safestring import SafeString

from . import engines as engines  # noqa: F401
from .backends.base import _EngineTemplate

def get_template(template_name: str, using: Optional[str] = ...) -> _EngineTemplate: ...
def select_template(template_name_list: Union[Sequence[str], str], using: Optional[str] = ...) -> Any: ...
def render_to_string(
    template_name: Union[Sequence[str], str],
    context: Optional[Mapping[str, Any]] = ...,
    request: Optional[HttpRequest] = ...,
    using: Optional[str] = ...,
) -> SafeString: ...
