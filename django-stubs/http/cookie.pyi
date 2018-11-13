# Stubs for django.http.cookie (Python 3.5)

from typing import Dict
from http.cookies import SimpleCookie, Morsel

cookie_pickles_properly = ...  # type: bool

def parse_cookie(cookie: str) -> Dict[str, str]: ...
