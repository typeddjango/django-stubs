from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.feedgenerator import Enclosure, SyndicationFeed

def add_domain(domain: str, url: str, secure: bool = ...) -> str: ...

class FeedDoesNotExist(ObjectDoesNotExist): ...

_Item = TypeVar("_Item", bound=Model)
_Object = TypeVar("_Object")

class Feed(Generic[_Item, _Object]):
    feed_type: Type[SyndicationFeed] = ...
    title_template: Optional[str] = ...
    description_template: Optional[str] = ...
    language: Optional[str] = ...

    # Dynamic attributes:
    title: Any
    link: Any
    feed_url: Any
    feed_guid: Any
    description: Any
    author_name: Any
    author_email: Any
    author_link: Any
    categories: Any
    feed_copyright: Any
    ttl: Any
    items: Any
    item_guid: Any
    item_guid_is_permalink: Any
    item_author_name: Any
    item_author_email: Any
    item_author_link: Any
    item_enclosure_url: Any
    item_enclosure_length: Any
    item_enclosure_mime_type: Any
    item_pubdate: Any
    item_updateddate: Any
    item_categories: Any
    item_copyright: Any
    item_comments: Any
    def __call__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_object(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Optional[_Object]: ...
    def feed_extra_kwargs(self, obj: _Object) -> Dict[Any, Any]: ...
    def item_extra_kwargs(self, item: _Item) -> Dict[Any, Any]: ...
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]: ...
    def get_feed(self, obj: _Object, request: HttpRequest) -> SyndicationFeed: ...
    def item_title(self, item: _Item) -> str: ...
    def item_description(self, item: _Item) -> str: ...
    def item_link(self, item: _Item) -> str: ...
    def item_enclosures(self, item: _Item) -> List[Enclosure]: ...
