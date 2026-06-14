from __future__ import annotations

import datetime

from django import http
from django.contrib import admin
from django.contrib.admin.options import _DisplayT
from django.contrib.admin.utils import (
    build_q_object_from_lookup_parameters,
    flatten,
    flatten_fieldsets,
    prepare_lookup_value,
)
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Upper
from typing_extensions import assert_type


@admin.display(description="Name")
def upper_case_name(obj: Person) -> str:
    return f"{obj.first_name} {obj.last_name}".upper()


class Person(models.Model):
    first_name = models.CharField(max_length=None)
    last_name = models.CharField(max_length=None)
    birthday = models.DateField()


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

# For some reason, pyright cannot see that these are not `None` so we need to ignore these for mypy.
assert person_list_admin.fields is not None  # type: ignore[comparison-overlap]
assert person_tuple_admin.fields is not None  # type: ignore[comparison-overlap]
assert person_fieldset_list_admin.fieldsets is not None  # type: ignore[comparison-overlap]
assert person_fieldset_tuple_admin.fieldsets is not None  # type: ignore[comparison-overlap]

assert_type(flatten(person_list_admin.fields), list[str])  # ty: ignore[no-matching-overload,type-assertion-failure]
assert_type(flatten(person_list_admin.get_fields(request)), list[str])
assert_type(flatten(person_tuple_admin.fields), list[str])
assert_type(flatten(person_tuple_admin.get_fields(request)), list[str])

assert_type(flatten(person_list_admin.list_display), list[_DisplayT[Person]])  # ty: ignore[no-matching-overload,type-assertion-failure]
assert_type(flatten(person_list_admin.get_list_display(request)), list[_DisplayT[Person]])  # ty: ignore[type-assertion-failure]
assert_type(flatten(person_tuple_admin.list_display), list[_DisplayT[Person]])  # ty: ignore[type-assertion-failure]
assert_type(flatten(person_tuple_admin.get_list_display(request)), list[_DisplayT[Person]])  # ty: ignore[type-assertion-failure]

assert_type(flatten_fieldsets(person_fieldset_list_admin.fieldsets), list[str])  # ty: ignore[invalid-argument-type]
assert_type(flatten_fieldsets(person_fieldset_list_admin.get_fieldsets(request)), list[str])
assert_type(flatten_fieldsets(person_fieldset_tuple_admin.fieldsets), list[str])  # ty: ignore[invalid-argument-type]
assert_type(flatten_fieldsets(person_fieldset_tuple_admin.get_fieldsets(request)), list[str])


class PersonOrderingAdmin(admin.ModelAdmin[Person]):
    ordering = [Upper("first_name")]


class PersonMixedOrderingAdmin(admin.ModelAdmin[Person]):
    ordering = ["-last_name", Upper("first_name")]


class PersonFExpressionAdmin(admin.ModelAdmin[Person]):
    ordering = [F("birthday").desc(nulls_last=True)]


# prepare_lookup_value: list[str] input recurses on each element,
# returning list[str] (pass-through) or list[bool] (__isnull keys)
assert_type(prepare_lookup_value("field", ["a", "b"]), list[str] | list[bool])

# str input: split (__in) -> list[str], bool (__isnull), or str (pass-through)
assert_type(prepare_lookup_value("field", "value"), str | bool | list[str])

# Non-str, non-list values pass through unchanged (e.g. datetime from date_hierarchy
# in ChangeList.get_filters)
assert_type(prepare_lookup_value("field", datetime.datetime.now()), datetime.datetime)


# Values are not limited to list[str] — any iterable of objects is accepted
assert_type(
    build_q_object_from_lookup_parameters(
        {
            "a": ["str"],
            "b": [datetime.datetime(2023, 1, 1)],
            "c": [True],
        }
    ),
    Q,
)
