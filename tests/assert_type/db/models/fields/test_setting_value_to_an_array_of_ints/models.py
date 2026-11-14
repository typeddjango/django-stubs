from __future__ import annotations

from django.contrib.postgres.fields import ArrayField
from django.db import models


class MyModel(models.Model):
    array = ArrayField(base_field=models.IntegerField())


def setting_value_to_an_array_of_ints() -> None:
    array_val: tuple[int, ...] = (1,)
    MyModel(array=array_val)
    array_val2: list[int] = [1]
    MyModel(array=array_val2)

    class NotAValid:
        pass

    array_val3: list[NotAValid] = [NotAValid()]
    MyModel(array=array_val3)  # type: ignore[misc]
    non_init = MyModel()
    non_init.array = array_val  # pyrefly: ignore[bad-assignment]
    non_init.array = array_val2
    non_init.array = array_val3  # type: ignore[assignment]
