"""`EmptyManager` reaches instances through `AnonymousUser.groups`, a plain property."""

from __future__ import annotations

from typing import assert_type

from django.contrib.auth.models import AnonymousUser, Group
from django.db.models.manager import EmptyManager


def empty_manager_access_through_property_is_allowed() -> None:
    assert_type(AnonymousUser().groups, EmptyManager[Group])
