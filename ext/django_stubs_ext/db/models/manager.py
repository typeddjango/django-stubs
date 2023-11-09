from typing import TYPE_CHECKING

# Re-export stubs-only classes RelatedManger and ManyRelatedManager.
# These are fake, Django defines these inside function body.
if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from django.db.models.fields.related_descriptors import ManyRelatedManager as ManyRelatedManager

    # noinspection PyUnresolvedReferences
    from django.db.models.fields.related_descriptors import RelatedManager as RelatedManager

else:
    from typing import Protocol, TypeVar

    _T = TypeVar("_T")

    # Define as `Protocol` to prevent them being used with `isinstance()`.
    # These actually inherit from `BaseManager`.
    class RelatedManager(Protocol[_T]):
        pass

    class ManyRelatedManager(Protocol[_T]):
        pass
