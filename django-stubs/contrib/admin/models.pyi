from collections.abc import Iterable
from datetime import datetime
from typing import Any, Literal, overload
from uuid import UUID

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model

ADDITION: int
CHANGE: int
DELETION: int
ACTION_FLAG_CHOICES: Any

class LogEntryManager(models.Manager[LogEntry]):
    @overload
    def log_actions(
        self,
        user_id: int | str | UUID,
        queryset: Iterable[Model],
        action_flag: int,
        change_message: str | list[Any] = "",
        *,
        single_object: Literal[True],
    ) -> LogEntry: ...
    @overload
    def log_actions(
        self,
        user_id: int | str | UUID,
        queryset: Iterable[Model],
        action_flag: int,
        change_message: str | list[Any] = "",
        *,
        single_object: Literal[False] = ...,
    ) -> list[LogEntry]: ...

class LogEntry(models.Model):
    action_time: models.DateTimeField[datetime, datetime]
    user: models.ForeignKey[User, User]
    content_type: models.ForeignKey[ContentType, ContentType]
    object_id: models.TextField[str, str]
    object_repr: models.CharField[str, str]
    action_flag: models.PositiveSmallIntegerField[int, int]
    change_message: models.TextField[str, str]
    objects: LogEntryManager  # type: ignore[assignment]
    def is_addition(self) -> bool: ...
    def is_change(self) -> bool: ...
    def is_deletion(self) -> bool: ...
    def get_change_message(self) -> str: ...
    def get_edited_object(self) -> Model: ...
    def get_admin_url(self) -> str | None: ...
