from typing import TYPE_CHECKING, ClassVar, Literal, Protocol, Sequence, Tuple, Union

from django.db.models import BaseConstraint, Index, OrderBy
from typing_extensions import TypeAlias

from django_stubs_ext import StrOrPromise

if TYPE_CHECKING:

    from typing import List

    class TypedModelMeta:
        """
        Typed base class for Django Model `class Meta:` inner class. At runtime this is just an alias to `object`.

        Most attributes are the same as `django.db.models.options.Options`. Options has some additional attributes and
        some values are normalized by Django.
        """

        abstract: ClassVar[bool]  # default: False
        app_label: ClassVar[str]
        base_manager_name: ClassVar[str]
        db_table: ClassVar[str]
        db_table_comment: ClassVar[str]
        db_tablespace: ClassVar[str]
        default_manager_name: ClassVar[str]
        default_related_name: ClassVar[str]
        get_latest_by: ClassVar[Union[str, Sequence[str]]]
        managed: ClassVar[bool]  # default: True
        order_with_respect_to: ClassVar[str]
        ordering: ClassVar[Sequence[Union[str, OrderBy]]]
        permissions: ClassVar[List[Tuple[str, str]]]
        default_permissions: ClassVar[Sequence[str]]  # default: ("add", "change", "delete", "view")
        proxy: ClassVar[bool]  # default: False
        required_db_features: ClassVar[List[str]]
        required_db_vendor: ClassVar[Literal["sqlite", "postgresql", "mysql", "oracle"]]
        select_on_save: ClassVar[bool]  # default: False
        indexes: ClassVar[List[Index]]
        unique_together: ClassVar[Union[Sequence[Sequence[str]], Sequence[str]]]
        index_together: ClassVar[Union[Sequence[Sequence[str]], Sequence[str]]]  # Deprecated in Django 4.2
        constraints: ClassVar[List[BaseConstraint]]
        verbose_name: ClassVar[StrOrPromise]
        verbose_name_plural: ClassVar[StrOrPromise]

else:
    TypedModelMeta = object


class _MetaAbstract(Protocol):
    abstract: ClassVar[bool]  # default: False


class _MetaAppLabel(Protocol):
    app_label: ClassVar[str]


class _MetaBaseManagerName(Protocol):
    base_manager_name: ClassVar[str]


class _MetaDbTable(Protocol):
    db_table: ClassVar[str]


class _MetaDbTableComment(Protocol):
    db_table_comment: ClassVar[str]


class _MetaDbTablespace(Protocol):
    db_tablespace: ClassVar[str]


class _MetaDefaultManagerName(Protocol):
    default_manager_name: ClassVar[str]


class _MetaDefaultRelatedName(Protocol):
    default_related_name: ClassVar[str]


class _MetaGetLatestBy(Protocol):
    get_latest_by: ClassVar[Union[str, Sequence[str]]]


class _MetaManaged(Protocol):
    managed: ClassVar[bool]  # default: True


class _MetaOrderWithRespectTo(Protocol):
    order_with_respect_to: ClassVar[str]


class _MetaOrdering(Protocol):
    ordering: ClassVar[Sequence[Union[str, OrderBy]]]


class _MetaPermissions(Protocol):
    permissions: ClassVar[Sequence[Tuple[str, str]]]


class _MetaDefaultPermissions(Protocol):
    default_permissions: ClassVar[Sequence[str]]  # default: ("add", "change", "delete", "view")


class _MetaProxy(Protocol):
    proxy: ClassVar[bool]  # default: False


class _MetaRequiredDbFeatures(Protocol):
    required_db_features: ClassVar[Sequence[str]]


class _MetaRequiredDbVendor(Protocol):
    required_db_vendor: ClassVar[Literal["sqlite", "postgresql", "mysql", "oracle"]]


class _MetaSelectOnSave(Protocol):
    select_on_save: ClassVar[bool]  # default: False


class _MetaIndexes(Protocol):
    indexes: ClassVar[Sequence[Index]]


class _MetaUniqueTogether(Protocol):
    unique_together: ClassVar[Union[Sequence[Sequence[str]], Sequence[str]]]


class _MetaIndexTogether(Protocol):
    index_together: ClassVar[Union[Sequence[Sequence[str]], Sequence[str]]]  # Deprecated in Django 4.2


class _MetaConstraints(Protocol):
    constraints: ClassVar[Sequence[BaseConstraint]]


class _MetaVerboseName(Protocol):
    verbose_name: ClassVar[StrOrPromise]


class _MetaVerboseNamePlural(Protocol):
    verbose_name_plural: ClassVar[StrOrPromise]


ModelMeta: TypeAlias = Union[
    _MetaAbstract,
    _MetaAppLabel,
    _MetaBaseManagerName,
    _MetaDbTable,
    _MetaDbTableComment,
    _MetaDbTablespace,
    _MetaDefaultManagerName,
    _MetaDefaultRelatedName,
    _MetaGetLatestBy,
    _MetaManaged,
    _MetaOrderWithRespectTo,
    _MetaOrdering,
    _MetaPermissions,
    _MetaDefaultPermissions,
    _MetaProxy,
    _MetaRequiredDbFeatures,
    _MetaRequiredDbVendor,
    _MetaSelectOnSave,
    _MetaIndexes,
    _MetaUniqueTogether,
    _MetaIndexTogether,
    _MetaConstraints,
    _MetaVerboseName,
    _MetaVerboseNamePlural,
]
