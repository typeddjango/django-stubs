from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.db import models

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import FileResponse, HttpRequest, HttpResponse


class DisplayModel(models.Model):
    @admin.display
    def display_bare(self) -> str:
        raise NotImplementedError

    @admin.display(ordering="field", description="Something", empty_value="...")
    def display_fancy(self) -> bool:
        raise NotImplementedError

    @property
    @admin.display
    def display_property(self) -> str:
        raise NotImplementedError


@admin.display
def freestanding_display_bare(obj: DisplayModel) -> str:
    raise NotImplementedError


@admin.display(boolean=True)
def freestanding_display_fancy(obj: DisplayModel) -> bool:
    raise NotImplementedError


@admin.register(DisplayModel, DisplayModel, site=None)
class DisplayModelAdmin(admin.ModelAdmin[DisplayModel]):
    list_display = [
        "display_property",
        "display_fancy",
        "display_bare",
        "admin_display_bare",
        "admin_display_fancy",
        freestanding_display_bare,
        freestanding_display_fancy,
    ]

    @admin.display
    def admin_display_bare(self, obj: DisplayModel) -> str:
        raise NotImplementedError

    @admin.display(boolean=True, ordering="field", description="Something")
    def admin_display_fancy(self, obj: DisplayModel) -> bool:
        raise NotImplementedError


# 'boolean' and 'empty_value' are mutually exclusive arguments
admin.display(lambda: 1, boolean=True, empty_value="str")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
admin.display(lambda: 1, boolean=False, empty_value="str")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
admin.display(boolean=True, empty_value="str")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
admin.display(boolean=False, empty_value="str")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]

# Valid combinations (function form)
admin.display(lambda: 1, boolean=True, empty_value=None)
admin.display(lambda: 1, boolean=False, empty_value=None)
admin.display(lambda: 1, boolean=True)
admin.display(lambda: 1, boolean=False)
admin.display(lambda: 1, boolean=None, empty_value="str")
admin.display(lambda: 1, boolean=None, empty_value=None)
admin.display(lambda: 1, empty_value="str")
admin.display(lambda: 1, empty_value=None)
admin.display(lambda: 1)

# Valid combinations (decorator form)
admin.display(boolean=True, empty_value=None)
admin.display(boolean=False, empty_value=None)
admin.display(boolean=True)
admin.display(boolean=False)
admin.display(boolean=None, empty_value="str")
admin.display(boolean=None, empty_value=None)
admin.display(empty_value="str")
admin.display(empty_value=None)
admin.display()


class ActionModel(models.Model): ...


@admin.action
def freestanding_action_bare(
    modeladmin: ActionModelAdmin, request: HttpRequest, queryset: QuerySet[ActionModel]
) -> None:
    raise NotImplementedError


@admin.action(description="Some text here", permissions=["test"])
def freestanding_action_fancy(
    modeladmin: ActionModelAdmin, request: HttpRequest, queryset: QuerySet[ActionModel]
) -> None:
    raise NotImplementedError


@admin.action
def freestanding_action_http_response(
    modeladmin: ActionModelAdmin, request: HttpRequest, queryset: QuerySet[ActionModel]
) -> HttpResponse:
    raise NotImplementedError


@admin.action
def freestanding_action_file_response(
    modeladmin: ActionModelAdmin, request: HttpRequest, queryset: QuerySet[ActionModel]
) -> FileResponse:
    raise NotImplementedError


@admin.register(ActionModel)
class ActionModelAdmin(admin.ModelAdmin[ActionModel]):
    actions = [  # pyrefly: ignore[bad-assignment]
        freestanding_action_bare,
        freestanding_action_fancy,
        "method_action_bare",
        "method_action_fancy",
        freestanding_action_http_response,
        freestanding_action_file_response,
    ]

    @admin.action
    def method_action_bare(self, request: HttpRequest, queryset: QuerySet[ActionModel]) -> None:
        raise NotImplementedError

    @admin.action(description="Some text here", permissions=["test"])
    def method_action_fancy(self, request: HttpRequest, queryset: QuerySet[ActionModel]) -> None:
        raise NotImplementedError

    @admin.action(description="Some text here", permissions=["test"])
    def method_action_http_response(self, request: HttpRequest, queryset: QuerySet[ActionModel]) -> HttpResponse:
        raise NotImplementedError

    @admin.action(description="Some text here", permissions=["test"])
    def method_action_file_response(self, request: HttpRequest, queryset: QuerySet[ActionModel]) -> FileResponse:
        raise NotImplementedError
