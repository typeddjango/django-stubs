from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.core.checks import CheckMessage, Warning, register
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.apps.config import AppConfig


@register("foo", deploy=True)
def check_foo(
    app_configs: Sequence[AppConfig] | None,
    databases: Sequence[str] | None,
    **kwargs: Any,
) -> list[Warning]:
    if databases and "databass" in databases:
        return [Warning("Naughty list")]
    return []


assert_type(check_foo.tags, Sequence[str])


@register
def check_bar(*, app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> list[CheckMessage]:
    raise NotImplementedError


assert_type(check_bar.tags, Sequence[str])


@register
def check_baz(**kwargs: Any) -> list[CheckMessage]:
    raise NotImplementedError


assert_type(check_baz.tags, Sequence[str])


@register()  # type: ignore[type-var]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-specialization]  # ty: ignore[invalid-argument-type]
def wrong_args(bla: int) -> list[CheckMessage]:
    raise NotImplementedError
