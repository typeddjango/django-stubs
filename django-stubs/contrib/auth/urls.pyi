from typing import List, Union

from django.urls import URLPattern, URLResolver

urlpatterns: List[Union[URLPattern, URLResolver]] = ...
