from typing import Any, Dict, Optional, Union
from uuid import UUID

from django.db.models.options import Options
from django.template.context import RequestContext
from django.utils.safestring import SafeText

register: Any

def admin_urlname(value: Options, arg: SafeText) -> str: ...
def admin_urlquote(value: Union[str, UUID, int]) -> Union[str, UUID, int]: ...
def add_preserved_filters(
    context: Union[Dict[str, Union[str, Options]], RequestContext],
    url: str,
    popup: bool = ...,
    to_field: Optional[str] = ...,
) -> str: ...
