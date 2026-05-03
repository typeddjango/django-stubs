from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib import admin, messages
from django.contrib.admin.sites import AdminSite
from django.core.paginator import Paginator
from django.db import models
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from typing_extensions import override

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.http.request import HttpRequest


# "Happy path" test for model admin, trying to cover as many valid
# configurations as possible.
class FullAdminModel(models.Model):
    pass


def full_admin_action(
    modeladmin: FullModelAdmin, request: HttpRequest, queryset: QuerySet[FullAdminModel, FullAdminModel]
) -> None:
    pass


class FullAdminModelForm(ModelForm[FullAdminModel]):
    pass


class FullModelAdmin(admin.ModelAdmin[FullAdminModel]):
    # BaseModelAdmin
    autocomplete_fields = ("strs",)
    raw_id_fields = ["strs"]
    fields = (
        "a field",
        ["a", "list of", "fields"],
    )
    exclude = ("a", "b")
    fieldsets = [
        (None, {"fields": ["a", "b"]}),
        ("group", {"fields": ("c",), "classes": ("a",), "description": "foo"}),
        (_("lazy"), {"fields": ["bar"]}),
    ]
    form = FullAdminModelForm
    filter_vertical = ("fields",)
    filter_horizontal = ("plenty", "of", "fields")
    radio_fields = {
        "some_field": admin.VERTICAL,
        "another_field": admin.HORIZONTAL,
    }
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {models.TextField: {"widget": Textarea}}  # pyright: ignore[reportUnknownVariableType]
    readonly_fields = ("date_modified",)
    ordering = ("-pk", "date_modified")
    sortable_by = ["pk"]
    view_on_site = True  # pyright: ignore[reportAssignmentType, reportIncompatibleMethodOverride]
    show_full_result_count = False

    # ModelAdmin
    list_display = ("pk",)
    list_display_links = ("str",)
    list_filter = ("str", admin.SimpleListFilter, ("str", admin.FieldListFilter))
    list_select_related = True
    list_per_page = 1
    list_max_show_all = 2
    list_editable = ("a", "b")
    search_fields = ("c", "d")
    date_hierarchy = "f"
    save_as = False
    save_as_continue = True
    save_on_top = False
    paginator = Paginator
    presserve_filters = False
    inlines = (admin.TabularInline, admin.StackedInline)
    add_form_template = "template"
    change_form_template = "template"
    change_list_template = "template"
    delete_confirmation_template = "template"
    delete_selected_confirmation_template = "template"
    object_history_template = "template"
    popup_response_template = "template"
    actions = (full_admin_action, "a_method_action")  # pyrefly: ignore[bad-assignment]
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    admin_site = AdminSite()

    # test generic ModelAdmin
    # https://github.com/typeddjango/django-stubs/pull/504
    # this will fail if `model` has a type other than the generic specified in the class declaration
    model = FullAdminModel

    def a_method_action(self, request: HttpRequest, queryset: QuerySet[FullAdminModel]) -> None:
        pass

    def a_method_action_with_message_user(self, request: HttpRequest, queryset: QuerySet[FullAdminModel]) -> None:
        self.message_user(request, _("Error message"), messages.ERROR)


# This admin is here to make sure we're not running into a mypy issue which is
# worked around using a somewhat complicated _ListOrTuple union type. Once the
# issue is solved upstream this test should pass even with the workaround
# replaced by a simpler Sequence type.
# https://github.com/python/mypy/issues/8921
class FieldsetWorkaroundAdmin(admin.ModelAdmin[Any]):
    fieldsets = (
        (
            None,
            {
                "fields": ("name",),
            },
        ),
    )


class ViewOnSiteCallableAdmin(admin.ModelAdmin[Any]):
    @override
    def view_on_site(self, obj: ViewOnSiteCallableAdmin) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        return "http://example.org"


class MissingFieldsetFieldsAdmin(admin.ModelAdmin[Any]):
    fieldsets = [
        (None, {}),  # type: ignore[typeddict-item]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-typed-dict-key]
    ]


class InvalidRadioFieldsValueAdmin(admin.ModelAdmin[Any]):
    radio_fields = {"some_field": 0}  # type: ignore[dict-item]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class InvalidRadioFieldsKeyAdmin(admin.ModelAdmin[Any]):
    radio_fields = {1: admin.VERTICAL}  # type: ignore[dict-item]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class InvalidFormfieldOverridesAdmin(admin.ModelAdmin[Any]):
    formfield_overrides = {  # pyrefly: ignore[bad-assignment]
        "not a field": {  # type: ignore[dict-item]  # pyright: ignore[reportAssignmentType]
            "widget": Textarea,
        }
    }


class InvalidActionSignatureModel(models.Model): ...


def invalid_action(modeladmin: None) -> None:
    pass


class InvalidActionSignatureAdmin(admin.ModelAdmin[InvalidActionSignatureModel]):
    actions = [invalid_action]  # type: ignore[list-item]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class InvalidGenericModel(models.Model):
    pass


class InvalidGenericModelAdmin(admin.ModelAdmin[InvalidGenericModel]):
    model = int  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]
