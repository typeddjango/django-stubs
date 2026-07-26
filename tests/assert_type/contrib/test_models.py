from __future__ import annotations

from datetime import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.redirects.models import Redirect
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from typing_extensions import assert_type


def log_entry_fields_are_inferred() -> None:
    entry = LogEntry()
    assert_type(entry.action_time, datetime)
    assert_type(entry.user, User)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(entry.content_type, ContentType | None)  # pyrefly: ignore[assert-type]
    assert_type(entry.object_id, str | None)  # pyrefly: ignore[assert-type]
    assert_type(entry.object_repr, str)
    assert_type(entry.action_flag, int)
    assert_type(entry.change_message, str)


def flatpage_fields_are_inferred() -> None:
    page = FlatPage()
    assert_type(page.url, str)
    assert_type(page.title, str)
    assert_type(page.content, str)
    assert_type(page.enable_comments, bool)
    assert_type(page.template_name, str)
    assert_type(page.registration_required, bool)
    assert_type(page.sites.get(), Site)  # pyright: ignore[reportUnknownMemberType]


def redirect_fields_are_inferred() -> None:
    redirect = Redirect()
    assert_type(redirect.site, Site)  # pyrefly: ignore[assert-type]
    assert_type(redirect.old_path, str)
    assert_type(redirect.new_path, str)


def site_fields_are_inferred() -> None:
    site = Site()
    assert_type(site.domain, str)
    assert_type(site.name, str)


def content_type_fields_are_inferred() -> None:
    content_type = ContentType()
    assert_type(content_type.app_label, str)
    assert_type(content_type.model, str)


def session_fields_are_inferred() -> None:
    session = Session()
    assert_type(session.session_key, str)
    assert_type(session.session_data, str)
    assert_type(session.expire_date, datetime)


def permission_fields_are_inferred() -> None:
    permission = Permission()
    assert_type(permission.name, str)
    assert_type(permission.content_type, ContentType)  # pyrefly: ignore[assert-type]
    assert_type(permission.codename, str)


def group_fields_are_inferred() -> None:
    group = Group()
    assert_type(group.name, str)
    assert_type(group.permissions.get(), Permission)  # pyright: ignore[reportUnknownMemberType]


def user_fields_are_inferred() -> None:
    user = User()
    assert_type(user.password, str)
    assert_type(user.last_login, datetime | None)  # pyrefly: ignore[assert-type]
    assert_type(user.username, str)
    assert_type(user.first_name, str)
    assert_type(user.last_name, str)
    assert_type(user.email, str)
    assert_type(user.is_staff, bool)
    assert_type(user.is_active, bool)
    assert_type(user.is_superuser, bool)
    assert_type(user.date_joined, datetime)
    assert_type(user.groups.get(), Group)  # pyright: ignore[reportUnknownMemberType]
    assert_type(user.user_permissions.get(), Permission)  # pyright: ignore[reportUnknownMemberType]
