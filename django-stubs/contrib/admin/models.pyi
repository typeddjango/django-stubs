from collections.abc import Iterable
from typing import Any, ClassVar, Literal, overload
from uuid import UUID

from django.conf import settings
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
    action_time = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField(blank=True)
    objects: ClassVar[LogEntryManager]
    def is_addition(self) -> bool: ...
    def is_change(self) -> bool: ...
    def is_deletion(self) -> bool: ...
    def get_change_message(self) -> str: ...
    def get_edited_object(self) -> Model: ...
    def get_admin_url(self) -> str | None: ...
