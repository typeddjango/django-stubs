from typing import Any
from uuid import UUID

from django.db import models
from django.db.models.base import Model

ADDITION: int
CHANGE: int
DELETION: int
ACTION_FLAG_CHOICES: Any

class LogEntryManager(models.Manager[LogEntry]):
    def log_action(
        self,
        user_id: int,
        content_type_id: int,
        object_id: int | str | UUID,
        object_repr: str,
        action_flag: int,
        change_message: Any = ...,
    ) -> LogEntry: ...

class LogEntry(models.Model):
    action_time: models.DateTimeField[Any, Any]
    user: models.ForeignKey[Any, Any]
    content_type: models.ForeignKey[Any, Any]
    object_id: models.TextField[Any, Any]
    object_repr: models.CharField[Any, Any]
    action_flag: models.PositiveSmallIntegerField[Any, Any]
    change_message: models.TextField[Any, Any]
    objects: LogEntryManager
    def is_addition(self) -> bool: ...
    def is_change(self) -> bool: ...
    def is_deletion(self) -> bool: ...
    def get_change_message(self) -> str: ...
    def get_edited_object(self) -> Model: ...
    def get_admin_url(self) -> str | None: ...
