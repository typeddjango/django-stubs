from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from typing import Union


def shortcut(
    request: HttpRequest,
    content_type_id: Union[str, int],
    object_id: Union[str, int]
) -> HttpResponseRedirect: ...