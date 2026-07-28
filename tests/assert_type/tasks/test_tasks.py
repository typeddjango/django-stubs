from __future__ import annotations

from typing import Any

from django.tasks import task
from django.tasks.base import Task, TaskContext, TaskResult
from typing_extensions import assert_type


@task
def test_task(x: int) -> int:
    return x + 1


assert_type(test_task.call(1), int)


@task(priority=5)
def test_task_with_priority(x: int) -> int:
    return x + 1


assert_type(test_task_with_priority.call(1), int)


@task(takes_context=True)
def test_task_with_context(context: TaskContext[Any, Any], x: int, /) -> int:
    return x + 1


assert_type(test_task_with_context, Task[[int], int])
assert_type(test_task_with_context.enqueue(1), TaskResult[[int], int])
assert_type(test_task_with_context.call(1), int)


@task(takes_context=True, priority=5)
def test_task_with_context_and_priority(context: TaskContext[Any, Any], x: int, /) -> int:
    return x + 1


assert_type(test_task_with_context_and_priority, Task[[int], int])
assert_type(test_task_with_context_and_priority.enqueue(1), TaskResult[[int], int])

assert_type(test_task_with_context.get_backend().enqueue(test_task_with_context, [1], {}), TaskResult[[int], int])
