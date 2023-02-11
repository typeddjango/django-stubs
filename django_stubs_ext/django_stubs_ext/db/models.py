from typing import ClassVar, Literal, Sequence

from django.db.models import BaseConstraint, Index

from django_stubs_ext import StrOrPromise


class BaseModelMeta:
    """
    Typed base class for Django Model `class Meta:` inner class.

    Most attributes are the same as `django.db.models.options.Options`. Options has some additional attributes and some
    values are normalized by Django.

    Usage::

        from django.db import models
        from django_stubs_ext.db.models import BaseModelMeta

        class MyModel(models.Model):
            example = models.CharField(max_length=100)

            class Meta(BaseModelMeta):
                ordering = ["example"]
    """

    abstract: ClassVar[bool]  # default: False
    app_label: ClassVar[str]
    base_manager_name: ClassVar[str]
    db_table: ClassVar[str]
    db_table_comment: ClassVar[str]
    db_tablespace: ClassVar[str]
    default_manager_name: ClassVar[str]
    default_related_name: ClassVar[str]
    get_latest_by: ClassVar[str | Sequence[str]]
    managed: ClassVar[bool]  # default: True
    order_with_respect_to: ClassVar[str]
    ordering: ClassVar[ClassVar[Sequence[str]]]
    permissions: ClassVar[list[tuple[str, str]]]
    default_permissions: ClassVar[Sequence[str]]  # default: ("add", "change", "delete", "view")
    proxy: ClassVar[bool]  # default: False
    required_db_features: ClassVar[list[str]]
    required_db_vendor: ClassVar[Literal["sqlite", "postgresql", "mysql", "oracle"]]
    select_on_save: ClassVar[bool]  # default: False
    indexes: ClassVar[list[Index]]
    unique_together: ClassVar[Sequence[Sequence[str]] | Sequence[str]]
    index_together: ClassVar[Sequence[Sequence[str]] | Sequence[str]]  # Deprecated in Django 4.2
    constraints: ClassVar[list[BaseConstraint]]
    verbose_name: ClassVar[StrOrPromise]
    verbose_name_plural: ClassVar[StrOrPromise]
