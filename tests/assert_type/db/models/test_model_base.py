"""The `ModelBase` metaclass properties, reached whenever a model class is only known as `type[_T]`."""

from __future__ import annotations

from typing import Generic, assert_type

from django.db import models
from typing_extensions import TypeVar

_T = TypeVar("_T", bound=models.Model)


class MyModel(models.Model):
    class Meta:
        app_label = "myapp"


class Base(Generic[_T]):
    def __init__(self, model_cls: type[_T]) -> None:
        self.model_cls = model_cls

    def test_unbound(self) -> None:
        # pyright reports `Manager[Model*]`: a conditional type still tied to `_T`, but not identical to it
        assert_type(self.model_cls._default_manager, models.Manager[_T])  # pyright: ignore[reportAssertTypeFailure]
        assert_type(self.model_cls._base_manager, models.Manager[_T])  # pyright: ignore[reportAssertTypeFailure]


class Child(Base[MyModel]):
    def test_bound(self) -> None:
        assert_type(self.model_cls._default_manager, models.Manager[MyModel])
        assert_type(self.model_cls._base_manager, models.Manager[MyModel])


assert_type(Base(MyModel).model_cls._default_manager, models.Manager[MyModel])
assert_type(Base(MyModel).model_cls._base_manager, models.Manager[MyModel])
