from __future__ import annotations

from datetime import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from typing_extensions import assert_type


def log_entry_fields_are_inferred() -> None:
    entry = LogEntry()
    assert_type(entry.action_time, datetime)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(entry.user, User)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(entry.content_type, ContentType | None)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(entry.object_id, str | None)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(entry.object_repr, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(entry.action_flag, int)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(entry.change_message, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


def flatpage_fields_are_inferred() -> None:
    page = FlatPage()
    assert_type(page.url, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.title, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.content, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.enable_comments, bool)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.template_name, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.registration_required, bool)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(page.sites.get(), Site)  # pyright: ignore[reportUnknownMemberType]


def redirect_fields_are_inferred() -> None:
    redirect = Redirect()
    assert_type(redirect.site, Site)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(redirect.old_path, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(redirect.new_path, str)  # pyright: ignore[reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
