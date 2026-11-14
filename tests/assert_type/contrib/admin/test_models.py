from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from django.contrib.admin.models import CHANGE, LogEntry

if TYPE_CHECKING:
    from django.contrib.auth.models import Group


def log_actions_returns_one_entry_per_object_unless_single_object(user_id: int, groups: list[Group]) -> None:
    assert_type(LogEntry.objects.log_actions(user_id, groups, CHANGE), list[LogEntry])
    assert_type(LogEntry.objects.log_actions(user_id, groups, CHANGE, single_object=True), LogEntry)
