from contextlib import contextmanager
from typing import Any, Generator, Type

from django.test import LiveServerTestCase

class SeleniumTestCaseBase:
    browsers: Any = ...
    browser: Any = ...
    @classmethod
    def import_webdriver(cls, browser: Any) -> Type[Any]: ...  # Type[WebDriver]
    def create_webdriver(self) -> Any: ...  # WebDriver

class SeleniumTestCase(LiveServerTestCase):
    implicit_wait: int = ...
    selenium: Any
    @contextmanager
    def disable_implicit_wait(self) -> Generator[None, None, None]: ...
