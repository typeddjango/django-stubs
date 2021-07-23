from typing import Any

from django_stubs_ext import ValuesQuerySet


def test_extends_values_queryset() -> None:
    class MyQS(ValuesQuerySet[Any, Any]):
        pass
