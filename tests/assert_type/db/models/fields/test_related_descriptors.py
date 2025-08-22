from typing import ClassVar

from django.db import models
from django.db.models.fields.related_descriptors import (
    RelatedManager,
    ReverseManyToOneDescriptor,
    create_reverse_many_to_one_manager,
)
from typing_extensions import assert_type


class Other(models.Model):
    explicit_descriptor: ClassVar[ReverseManyToOneDescriptor["MyModel"]]


class MyModel(models.Model):
    rel = models.ForeignKey[Other, Other](Other, on_delete=models.CASCADE, related_name="explicit_descriptor")


assert_type(Other().explicit_descriptor, RelatedManager[MyModel, models.QuerySet[MyModel, MyModel]])

# Ensure `create_reverse_many_to_one_manager` pass generic params correctly
reverse_many_to_one_manager = create_reverse_many_to_one_manager(
    superclass=MyModel._default_manager.__class__, rel=MyModel.rel.field.remote_field
)
assert_type(MyModel._default_manager.__class__, type[models.Manager[MyModel, models.QuerySet[MyModel, MyModel]]])
assert_type(reverse_many_to_one_manager, type[RelatedManager[MyModel, models.QuerySet[MyModel, MyModel]]])
