from typing import List, Optional, Union

from django.urls import URLPattern, URLResolver

urlpatterns: List[Union[URLPattern, URLResolver]] = ...

def staticfiles_urlpatterns(prefix: Optional[str] = ...) -> List[URLPattern]: ...
