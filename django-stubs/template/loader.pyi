from typing import Dict, List, Optional, Union, Any

from django.core.handlers.wsgi import WSGIRequest
from . import engines as engines

def get_template(template_name: str, using: Optional[str] = ...) -> Any: ...
def select_template(template_name_list: Union[List[str], str], using: Optional[str] = ...) -> Any: ...
def render_to_string(
    template_name: Union[List[str], str],
    context: Optional[Dict[str, Any]] = ...,
    request: Optional[WSGIRequest] = ...,
    using: Optional[str] = ...,
) -> str: ...
