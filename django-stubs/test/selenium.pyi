from contextlib import AbstractContextManager
from typing import Any

from django.test import LiveServerTestCase

class SeleniumTestCaseBase:
    browsers: Any
    browser: Any
    @classmethod
    def import_webdriver(cls, browser: Any) -> type[Any]: ...  # Type[WebDriver]
    def create_webdriver(self) -> Any: ...  # WebDriver

class SeleniumTestCase(LiveServerTestCase):
    implicit_wait: int
    selenium: Any
    def disable_implicit_wait(self) -> AbstractContextManager[None]: ...
