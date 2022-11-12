from typing import List

from django.urls import URLPattern, _AnyURL

urlpatterns: List[_AnyURL] = ...

def staticfiles_urlpatterns(prefix: str | None = ...) -> List[URLPattern]: ...
