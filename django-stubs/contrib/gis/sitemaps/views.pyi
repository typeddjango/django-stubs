from typing import Optional

from django.http import HttpRequest, HttpResponse

def kml(
    request: HttpRequest,
    label: str,
    model: str,
    field_name: Optional[str] = ...,
    compress: bool = ...,
    using: str = ...,
) -> HttpResponse: ...
def kmz(
    request: HttpRequest, label: str, model: str, field_name: Optional[str] = ..., using: str = ...
) -> HttpResponse: ...
