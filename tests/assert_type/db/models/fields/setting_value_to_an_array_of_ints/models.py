from __future__ import annotations

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F


class MyModel(models.Model):
    array = ArrayField(base_field=models.IntegerField())


non_init = MyModel()


def setting_value_to_a_tuple_of_ints_ok() -> None:
    array_val: tuple[int, ...] = (1,)
    MyModel(array=array_val)
    non_init.array = array_val


def setting_value_to_an_array_of_ints_ok() -> None:
    array_val2: list[int] = [1]
    MyModel(array=array_val2)
    non_init.array = array_val2


def setting_value_to_an_array_of_invalid_type_error() -> None:
    class NotAValid:
        pass

    array_val3: list[NotAValid] = [NotAValid()]
    MyModel(array=array_val3)  # type: ignore[misc]
    non_init.array = array_val3  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue] # ty:ignore[invalid-assignment] # pyrefly: ignore[no-matching-overload]


def setting_value_to_an_array_of_combinable_error() -> None:
    array_val4: list[F] = [F("id")]
    MyModel(array=array_val4)  # type: ignore[misc]
    non_init.array = array_val4  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue] # ty:ignore[invalid-assignment] # pyrefly: ignore[no-matching-overload]
