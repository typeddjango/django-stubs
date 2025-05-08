import builtins
import logging
from collections.abc import Iterable
from typing import Any, Generic, TypeVar

from django import VERSION
from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed
from django.core.exceptions import AppRegistryNotReady, ImproperlyConfigured
from django.core.files.utils import FileProxyMixin
from django.core.paginator import Paginator
from django.db.models.expressions import ExpressionWrapper
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from django.db.models.lookups import Lookup
from django.db.models.manager import BaseManager
from django.db.models.options import Options
from django.db.models.query import BaseIterable, ModelIterable, QuerySet, RawQuerySet
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseModelForm, BaseModelFormSet, ModelChoiceField, ModelFormOptions
from django.utils.connection import BaseConnectionHandler, ConnectionProxy
from django.utils.functional import classproperty
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin, FormMixin
from django.views.generic.list import MultipleObjectMixin

__all__ = ["monkeypatch"]

logger = logging.getLogger(__name__)

_T = TypeVar("_T")
_VersionSpec = tuple[int, int]


class MPGeneric(Generic[_T]):
    """Create a data class to hold metadata about the generic classes needing monkeypatching.

    The `version` param is optional, and a value of `None` means that the monkeypatch is
    version-independent.

    This is slightly overkill for our purposes, but useful for future-proofing against any
    possible issues we may run into with this method.
    """

    def __init__(self, cls: type[_T], version: _VersionSpec | None = None) -> None:
        """Set the data fields, basic constructor."""
        self.version = version
        self.cls = cls

    def __repr__(self) -> str:
        """Better representation in tests and debug."""
        return "<MPGeneric: {}, versions={}>".format(self.cls, self.version or "all")


# certain django classes need to be generic, but lack the __class_getitem__ dunder needed to
# annotate them: https://github.com/typeddjango/django-stubs/issues/507
# this list stores them so `monkeypatch` can fix them when called
_need_generic: list[MPGeneric[Any]] = [
    MPGeneric(ModelAdmin),
    MPGeneric(SingleObjectMixin),
    MPGeneric(FormMixin),
    MPGeneric(DeletionMixin),
    MPGeneric(MultipleObjectMixin),
    MPGeneric(BaseModelAdmin),
    MPGeneric(Field),
    MPGeneric(Paginator),
    MPGeneric(BaseFormSet),
    MPGeneric(BaseModelForm),
    MPGeneric(BaseModelFormSet),
    MPGeneric(ModelChoiceField),
    MPGeneric(Feed),
    MPGeneric(Sitemap),
    MPGeneric(SuccessMessageMixin),
    MPGeneric(FileProxyMixin),
    MPGeneric(Lookup),
    MPGeneric(BaseConnectionHandler),
    MPGeneric(ExpressionWrapper),
    MPGeneric(ReverseManyToOneDescriptor),
    MPGeneric(ModelIterable),
    # These types do have native `__class_getitem__` method since django 3.1:
    MPGeneric(QuerySet, (3, 1)),
    MPGeneric(BaseManager, (3, 1)),
    # These types do have native `__class_getitem__` method since django 4.1:
    MPGeneric(ForeignKey, (4, 1)),
    MPGeneric(RawQuerySet),
    MPGeneric(classproperty),
    MPGeneric(ConnectionProxy),
    MPGeneric(ModelFormOptions),
    MPGeneric(Options),
    MPGeneric(BaseIterable),
    MPGeneric(ForwardManyToOneDescriptor),
    MPGeneric(ReverseOneToOneDescriptor),
]


def _get_need_generic() -> list[MPGeneric[Any]]:
    try:
        if VERSION >= (5, 1):
            from django.contrib.auth.forms import SetPasswordMixin, SetUnusablePasswordMixin

            return [MPGeneric(SetPasswordMixin), MPGeneric(SetUnusablePasswordMixin), *_need_generic]
        else:
            from django.contrib.auth.forms import AdminPasswordChangeForm, SetPasswordForm

            return [MPGeneric(SetPasswordForm), MPGeneric(AdminPasswordChangeForm), *_need_generic]

    except (ImproperlyConfigured, AppRegistryNotReady):
        # We cannot patch symbols in `django.contrib.auth.forms` if the `monkeypatch()` call
        # is in the settings file because django is not initialized yet.
        # To solve this, you'll have to call `monkeypatch()` again later, in an `AppConfig.ready` for ex.
        # See https://docs.djangoproject.com/en/5.2/ref/applications/#django.apps.AppConfig.ready
        return _need_generic


def monkeypatch(extra_classes: Iterable[type] | None = None, include_builtins: bool = True) -> None:
    """Monkey patch django as necessary to work properly with mypy."""
    # Add the __class_getitem__ dunder.
    suited_for_this_version = filter(
        lambda spec: spec.version is None or VERSION[:2] <= spec.version,
        _get_need_generic(),
    )
    for el in suited_for_this_version:
        el.cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
    if extra_classes:
        for cls in extra_classes:
            cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined]

    # Add `reveal_type` and `reveal_locals` helpers if needed:
    if include_builtins:
        builtins.reveal_type = lambda _: None
        builtins.reveal_locals = lambda: None
