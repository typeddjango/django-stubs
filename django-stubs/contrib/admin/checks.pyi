from collections.abc import Sequence
from typing import Any

from django.apps.config import AppConfig
from django.contrib.admin.options import BaseModelAdmin
from django.core.checks.messages import CheckMessage
from typing_extensions import override

def check_admin_app(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> list[CheckMessage]: ...
def check_dependencies(**kwargs: Any) -> list[CheckMessage]: ...

class BaseModelAdminChecks:
    def check(self, admin_obj: BaseModelAdmin[Any], **kwargs: Any) -> list[CheckMessage]: ...

class ModelAdminChecks(BaseModelAdminChecks): ...

class InlineModelAdminChecks(BaseModelAdminChecks):
    # We need this override because `InlineModelAdminChecks` rename `admin_obj` to `inline_obj` here
    @override
    def check(self, inline_obj: BaseModelAdmin[Any], **kwargs: Any) -> list[CheckMessage]: ...  # type: ignore[override]

def must_be(type: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
def must_inherit_from(parent: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
def refer_to_missing_field(field: Any, option: Any, obj: Any, id: Any) -> list[CheckMessage]: ...
