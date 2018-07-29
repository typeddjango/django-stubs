from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.http.response import HttpResponse
from django.utils.feedgenerator import (
    Atom1Feed,
    Enclosure,
    Rss201rev2Feed,
)
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


def add_domain(domain: str, url: str, secure: bool = ...) -> str: ...


class Feed:
    def __call__(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponse: ...
    def _get_dynamic_attr(
        self,
        attname: str,
        obj: Optional[Model],
        default: Optional[str] = ...
    ) -> Any: ...
    def feed_extra_kwargs(self, obj: None) -> Dict[Any, Any]: ...
    def get_context_data(self, **kwargs) -> Dict[str, Model]: ...
    def get_feed(
        self,
        obj: None,
        request: WSGIRequest
    ) -> Union[Atom1Feed, Rss201rev2Feed]: ...
    def get_object(self, request: WSGIRequest, *args, **kwargs) -> None: ...
    def item_description(self, item: Model) -> str: ...
    def item_enclosures(self, item: Model) -> List[Enclosure]: ...
    def item_extra_kwargs(self, item: Model) -> Dict[Any, Any]: ...
    def item_link(self, item: Model) -> str: ...
    def item_title(self, item: Model) -> SafeText: ...