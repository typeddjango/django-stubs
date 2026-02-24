from collections.abc import Iterable
from datetime import datetime
from typing import Any, ClassVar, Literal, overload
from uuid import UUID

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.query_utils import DeferredAttribute

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
    action_time: DeferredAttribute | models.DateTimeField[datetime, datetime]
    user: ForwardManyToOneDescriptor[models.ForeignKey[User, User]] | models.ForeignKey[User, User]
    content_type: (
        ForwardManyToOneDescriptor[models.ForeignKey[ContentType, ContentType]]
        | models.ForeignKey[ContentType, ContentType]
    )
    object_id: DeferredAttribute | models.TextField[str, str]
    object_repr: DeferredAttribute | models.CharField[str, str]
    action_flag: DeferredAttribute | models.PositiveSmallIntegerField[int, int]
    change_message: DeferredAttribute | models.TextField[str, str]
    objects: ClassVar[LogEntryManager]
    def is_addition(self) -> bool: ...
    def is_change(self) -> bool: ...
    def is_deletion(self) -> bool: ...
    def get_change_message(self) -> str: ...
    def get_edited_object(self) -> Model: ...
    def get_admin_url(self) -> str | None: ...
