from datetime import datetime

from django.contrib.admin.models import LogEntry, LogEntryManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from typing_extensions import assert_type

log_entry = LogEntry()
assert_type(log_entry.id, int)
assert_type(log_entry.pk, int)
assert_type(log_entry.action_time, datetime)
assert_type(log_entry.user, AbstractUser)
assert_type(log_entry.content_type, ContentType | None)
assert_type(log_entry.content_type_id, int | None)
assert_type(log_entry.object_id, str | None)
assert_type(log_entry.object_repr, str)
assert_type(log_entry.action_flag, int)
assert_type(log_entry.change_message, str)
assert_type(log_entry.user_id, int)
assert_type(LogEntry.objects, LogEntryManager)
