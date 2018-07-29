from django.db.backends.dummy.base import DatabaseWrapper
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.test.testcases import (
    SimpleTestCase,
    TestCase,
)
from django.utils.datastructures import OrderedSet
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
from unittest.case import _SubTest
from unittest.runner import TextTestResult
from unittest.suite import TestSuite


def default_test_processes() -> int: ...


def filter_tests_by_tags(
    suite: TestSuite,
    tags: Set[str],
    exclude_tags: Set[str]
) -> TestSuite: ...


def is_discoverable(label: str) -> bool: ...


def partition_suite_by_type(
    suite: TestSuite,
    classes: Tuple[Type[TestCase], Type[SimpleTestCase]],
    bins: List[OrderedSet],
    reverse: bool = ...
) -> None: ...


def reorder_suite(
    suite: TestSuite,
    classes: Tuple[Type[TestCase], Type[SimpleTestCase]],
    reverse: bool = ...
) -> TestSuite: ...


class DebugSQLTextTestResult:
    def addSubTest(self, test: TestCase, subtest: _SubTest, err: None) -> None: ...
    def printErrorList(
        self,
        flavour: str,
        errors: List[Union[Tuple[TestCase, str, str], Tuple[_SubTest, str, str]]]
    ) -> None: ...
    def startTest(self, test: TestCase) -> None: ...
    def stopTest(self, test: TestCase) -> None: ...


class DiscoverRunner:
    def __init__(
        self,
        pattern: None = ...,
        top_level: None = ...,
        verbosity: int = ...,
        interactive: bool = ...,
        failfast: bool = ...,
        keepdb: bool = ...,
        reverse: bool = ...,
        debug_mode: bool = ...,
        debug_sql: bool = ...,
        parallel: int = ...,
        tags: Optional[List[str]] = ...,
        exclude_tags: None = ...,
        **kwargs
    ) -> None: ...
    def build_suite(
        self,
        test_labels: Union[Tuple[str, str], List[str], Tuple[str]] = ...,
        extra_tests: None = ...,
        **kwargs
    ) -> TestSuite: ...
    def get_resultclass(self) -> None: ...
    def get_test_runner_kwargs(self) -> Dict[str, Optional[int]]: ...
    def run_checks(self) -> None: ...
    def run_suite(self, suite: TestSuite, **kwargs) -> TextTestResult: ...
    def run_tests(self, test_labels: List[str], extra_tests: List[Any] = ..., **kwargs) -> int: ...
    def setup_databases(
        self,
        **kwargs
    ) -> Union[List[Tuple[DatabaseWrapper, str, bool]], List[Tuple[DatabaseWrapper, str, bool]]]: ...
    def setup_test_environment(self, **kwargs) -> None: ...
    def suite_result(self, suite: TestSuite, result: TextTestResult, **kwargs) -> int: ...
    def teardown_databases(
        self,
        old_config: Union[List[Tuple[DatabaseWrapper, str, bool]], List[Tuple[DatabaseWrapper, str, bool]]],
        **kwargs
    ) -> None: ...
    def teardown_test_environment(self, **kwargs) -> None: ...