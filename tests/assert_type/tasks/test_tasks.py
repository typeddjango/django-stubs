from __future__ import annotations

from django.tasks import task
from typing_extensions import assert_type


@task
def test_task(x: int) -> int:
    return x + 1


assert_type(test_task.call(1), int)


@task(priority=5)
def test_task_with_priority(x: int) -> int:
    return x + 1


assert_type(test_task_with_priority.call(1), int)
