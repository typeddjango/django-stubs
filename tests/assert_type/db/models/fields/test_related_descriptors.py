from typing import ClassVar

from django.db import models
from django.db.models.fields.related_descriptors import RelatedManager, ReverseManyToOneDescriptor
from typing_extensions import assert_type


class Other(models.Model):
    explicit_descriptor: ClassVar[ReverseManyToOneDescriptor["MyModel"]]


class MyModel(models.Model):
    rel = models.ForeignKey[Other, Other](Other, on_delete=models.CASCADE, related_name="explicit_descriptor")


# Pyright doesn't allow "runtime" usage of @type_check_only 'RelatedManager' but we're
# only type checking these files so it should be fine.
assert_type(Other().explicit_descriptor, RelatedManager[MyModel])  # pyright: ignore[reportGeneralTypeIssues]
