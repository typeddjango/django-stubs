from datetime import date, datetime
from typing import Any, ClassVar
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model
from django.db.models.expressions import Combinable

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
    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    action_time: models.DateTimeField[str | datetime | date | Combinable, datetime]
    user: models.ForeignKey[AbstractUser | Combinable, AbstractUser]
    user_id: Any
    content_type: models.ForeignKey[ContentType | Combinable | None, ContentType | None]
    content_type_id: int | None
    object_id: models.TextField[str | int | Combinable | None, str | None]
    object_repr: models.CharField[str | int | Combinable, str]
    action_flag: models.PositiveSmallIntegerField[float | int | str | Combinable, int]
    change_message: models.TextField[str | int | Combinable, str]
    objects: ClassVar[LogEntryManager]
    def is_addition(self) -> bool: ...
    def is_change(self) -> bool: ...
    def is_deletion(self) -> bool: ...
    def get_change_message(self) -> str: ...
    def get_edited_object(self) -> Model: ...
    def get_admin_url(self) -> str | None: ...
