from __future__ import annotations

from django import http
from django.contrib import admin
from django.contrib.admin.options import _DisplayT
from django.contrib.admin.utils import flatten, flatten_fieldsets
from django.db import models
from typing_extensions import assert_type


@admin.display(description="Name")
def upper_case_name(obj: Person) -> str:
    return f"{obj.first_name} {obj.last_name}".upper()  # pyright: ignore[reportUnknownMemberType]


class Person(models.Model):
    first_name = models.CharField(max_length=None)  # pyright: ignore[reportUnknownVariableType]
    last_name = models.CharField(max_length=None)  # pyright: ignore[reportUnknownVariableType]
    birthday = models.DateField()  # pyright: ignore[reportUnknownVariableType]


class PersonListAdmin(admin.ModelAdmin[Person]):
    fields = [["first_name", "last_name"], "birthday"]
    list_display = [upper_case_name, "birthday"]


class PersonTupleAdmin(admin.ModelAdmin[Person]):
    fields = (("first_name", "last_name"), "birthday")
    list_display = (upper_case_name, "birthday")


class PersonFieldsetListAdmin(admin.ModelAdmin[Person]):
    fieldsets = [
        (
            "Personal Details",
            {
                "description": "Personal details of a person.",
                "fields": [["first_name", "last_name"], "birthday"],
            },
        )
    ]


class PersonFieldsetTupleAdmin(admin.ModelAdmin[Person]):
    fieldsets = (
        (
            "Personal Details",
            {
                "description": "Personal details of a person.",
                "fields": (("first_name", "last_name"), "birthday"),
            },
        ),
    )


request = http.HttpRequest()
admin_site = admin.AdminSite()
person_list_admin = PersonListAdmin(Person, admin_site)
person_tuple_admin = PersonTupleAdmin(Person, admin_site)
person_fieldset_list_admin = PersonFieldsetListAdmin(Person, admin_site)
person_fieldset_tuple_admin = PersonFieldsetTupleAdmin(Person, admin_site)

# For some reason, pyright cannot see that these are not `None`.
assert person_list_admin.fields is not None
assert person_tuple_admin.fields is not None
assert person_fieldset_list_admin.fieldsets is not None
assert person_fieldset_tuple_admin.fieldsets is not None

assert_type(flatten(person_list_admin.fields), list[str])
assert_type(flatten(person_list_admin.get_fields(request)), list[str])
assert_type(flatten(person_tuple_admin.fields), list[str])
assert_type(flatten(person_tuple_admin.get_fields(request)), list[str])

assert_type(flatten(person_list_admin.list_display), list[_DisplayT[Person]])
assert_type(flatten(person_list_admin.get_list_display(request)), list[_DisplayT[Person]])
assert_type(flatten(person_tuple_admin.list_display), list[_DisplayT[Person]])
assert_type(flatten(person_tuple_admin.get_list_display(request)), list[_DisplayT[Person]])

assert_type(flatten_fieldsets(person_fieldset_list_admin.fieldsets), list[str])
assert_type(flatten_fieldsets(person_fieldset_list_admin.get_fieldsets(request)), list[str])
assert_type(flatten_fieldsets(person_fieldset_tuple_admin.fieldsets), list[str])
assert_type(flatten_fieldsets(person_fieldset_tuple_admin.get_fieldsets(request)), list[str])
