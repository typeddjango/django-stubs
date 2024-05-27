from django.apps.config import AppConfig
from django.utils.functional import cached_property
from typing_extensions import assert_type


class FooConfig(AppConfig):
    name = "foo"
    default_auto_field = "django.db.models.BigAutoField"


class BarConfig(AppConfig):
    name = "foo"

    @property
    def default_auto_field(self) -> str:  # type: ignore[override]
        return "django.db.models.BigAutoField"


class BazConfig(AppConfig):
    name = "foo"

    @cached_property
    def default_auto_field(self) -> str:  # type: ignore[override]
        return "django.db.models.BigAutoField"


class FooBarConfig(AppConfig):
    name = "foo"
    default_auto_field = cached_property(lambda self: "django.db.models.BigAutoField")


# Pyright correctly picks up our fake '_Getter' descriptor on class level. But we
# silence the pyright error since mypy doesn't follow along and the fake descriptor
# is a stubs detail made to round other problems.
assert_type(FooConfig.default_auto_field, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(BarConfig("bar", None).default_auto_field, str)
assert_type(BazConfig("baz", None).default_auto_field, str)
assert_type(FooBarConfig("baz", None).default_auto_field, str)
