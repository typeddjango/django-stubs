from typing import List, Optional

from django.urls import URLPattern, _AnyURL

urlpatterns: List[_AnyURL] = ...

def staticfiles_urlpatterns(prefix: Optional[str] = ...) -> List[URLPattern]: ...
