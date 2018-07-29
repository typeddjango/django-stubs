from django.contrib.admin.tests import AdminSeleniumTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from typing import (
    Callable,
    Dict,
    List,
    Tuple,
    Type,
    Union,
)


class SeleniumTestCaseBase:
    @staticmethod
    def __new__(
        cls: Type[SeleniumTestCaseBase],
        name: str,
        bases: Union[Tuple[Type[AdminSeleniumTestCase]], Tuple[Type[SeleniumTestCase], Type[StaticLiveServerTestCase]]],
        attrs: Dict[str, Union[str, List[str], Callable]]
    ) -> Type[AdminSeleniumTestCase]: ...