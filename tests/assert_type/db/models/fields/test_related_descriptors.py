from __future__ import annotations

from typing import ClassVar

from django.db import models
from django.db.models.fields.related_descriptors import RelatedManager, ReverseManyToOneDescriptor
from typing_extensions import TypeVar, assert_type

_To = TypeVar("_To", bound=models.Model)


class Other(models.Model):
    explicit_descriptor: ClassVar[ReverseManyToOneDescriptor[MyModel]]


class MyModel(models.Model):
    rel = models.ForeignKey[Other, Other](Other, on_delete=models.CASCADE, related_name="explicit_descriptor")


assert_type(Other().explicit_descriptor, RelatedManager[MyModel])


class CustomDescriptor(ReverseManyToOneDescriptor[MyModel]):
    def custom_method(self) -> int:
        raise NotImplementedError


class WithCustomDescriptor(models.Model):
    custom_descriptor: ClassVar[CustomDescriptor]


# Class-level access returns `Self`, preserving descriptor subclasses and their members
assert_type(WithCustomDescriptor.custom_descriptor, CustomDescriptor)
assert_type(WithCustomDescriptor.custom_descriptor.custom_method(), int)


class PassThroughDescriptor(ReverseManyToOneDescriptor[_To]): ...


class WithPassThroughDescriptor(models.Model):
    passthrough_descriptor: ClassVar[PassThroughDescriptor[MyModel]]


# Class-level access returns `Self`, preserving a generic subclass and its parameterization
assert_type(WithPassThroughDescriptor.passthrough_descriptor, PassThroughDescriptor[MyModel])

assert_type(MyModel._default_manager.__class__, type[models.Manager[MyModel]])
