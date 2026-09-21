"""A protocol can declare a manager attribute, its implementers are not model instances."""

from __future__ import annotations

from typing import Protocol, assert_type

from django.contrib.auth.models import Group
from django.db import models


class PermissionAware(Protocol):
    groups: models.Manager[Group]


def manager_on_protocol_is_allowed(user: PermissionAware) -> None:
    assert_type(user.groups, models.Manager[Group])
