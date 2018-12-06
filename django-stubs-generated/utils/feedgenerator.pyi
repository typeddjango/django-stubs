from datetime import date, datetime
from io import StringIO
from typing import Any, Dict, List, Optional, Tuple, Union

from django.http.response import HttpResponse
from django.utils.xmlutils import SimplerXMLGenerator

def rfc2822_date(date: date) -> str: ...
def rfc3339_date(date: date) -> str: ...
def get_tag_uri(url: str, date: Optional[date]) -> str: ...

class SyndicationFeed:
    feed: Any = ...
    items: Any = ...
    def __init__(
        self,
        title: str,
        link: str,
        description: Optional[str],
        language: Optional[str] = ...,
        author_email: Optional[str] = ...,
        author_name: Optional[str] = ...,
        author_link: Optional[str] = ...,
        subtitle: Optional[str] = ...,
        categories: Optional[Tuple[str, str]] = ...,
        feed_url: Optional[str] = ...,
        feed_copyright: Optional[str] = ...,
        feed_guid: Optional[str] = ...,
        ttl: Optional[int] = ...,
        **kwargs: Any
    ) -> None: ...
    def add_item(
        self,
        title: str,
        link: str,
        description: str,
        author_email: Optional[str] = ...,
        author_name: Optional[str] = ...,
        author_link: Optional[str] = ...,
        pubdate: Optional[datetime] = ...,
        comments: None = ...,
        unique_id: Optional[str] = ...,
        unique_id_is_permalink: Optional[bool] = ...,
        categories: Optional[Tuple] = ...,
        item_copyright: Optional[str] = ...,
        ttl: None = ...,
        updateddate: Optional[datetime] = ...,
        enclosures: Optional[List[Enclosure]] = ...,
        **kwargs: Any
    ) -> None: ...
    def num_items(self): ...
    def root_attributes(self) -> Dict[Any, Any]: ...
    def add_root_elements(self, handler: Any) -> None: ...
    def item_attributes(self, item: Dict[str, Any]) -> Dict[Any, Any]: ...
    def add_item_elements(self, handler: Any, item: Any) -> None: ...
    def write(self, outfile: Any, encoding: Any) -> None: ...
    def writeString(self, encoding: str) -> str: ...
    def latest_post_date(self) -> datetime: ...

class Enclosure:
    length: Union[int, str]
    mime_type: str
    url: str = ...
    def __init__(self, url: str, length: Union[int, str], mime_type: str) -> None: ...

class RssFeed(SyndicationFeed):
    content_type: str = ...
    def write(self, outfile: Union[StringIO, HttpResponse], encoding: str) -> None: ...
    def rss_attributes(self) -> Dict[str, str]: ...
    def write_items(self, handler: SimplerXMLGenerator) -> None: ...
    def add_root_elements(self, handler: SimplerXMLGenerator) -> None: ...
    def endChannelElement(self, handler: SimplerXMLGenerator) -> None: ...

class RssUserland091Feed(RssFeed):
    feed: Dict[str, Optional[Union[List[str], str]]]
    items: List[Dict[str, Optional[Union[List[str], Tuple, datetime.datetime, str]]]]
    def add_item_elements(
        self, handler: SimplerXMLGenerator, item: Dict[str, Optional[Union[List[str], Tuple, datetime, str]]]
    ) -> None: ...

class Rss201rev2Feed(RssFeed):
    feed: Dict[str, Optional[Union[List[str], Tuple, str]]]
    items: Union[
        List[Dict[str, Any]],
        List[Dict[str, Optional[Union[List[django.utils.feedgenerator.Enclosure], List[str], datetime.datetime, str]]]],
    ]
    def add_item_elements(self, handler: SimplerXMLGenerator, item: Dict[str, Any]) -> None: ...

class Atom1Feed(SyndicationFeed):
    feed: Dict[str, Optional[Union[List[str], Tuple, str]]]
    items: Union[
        List[Dict[str, Optional[Union[List[django.utils.feedgenerator.Enclosure], List[str], datetime.datetime, str]]]],
        List[Dict[str, Optional[Union[List[str], Tuple, datetime.datetime, str]]]],
    ]
    content_type: str = ...
    ns: str = ...
    def write(self, outfile: Union[StringIO, HttpResponse], encoding: str) -> None: ...
    def root_attributes(self) -> Dict[str, str]: ...
    def add_root_elements(self, handler: SimplerXMLGenerator) -> None: ...
    def write_items(self, handler: SimplerXMLGenerator) -> None: ...
    def add_item_elements(
        self,
        handler: SimplerXMLGenerator,
        item: Dict[str, Optional[Union[List[Enclosure], List[str], Tuple, datetime, str]]],
    ) -> None: ...

DefaultFeed = Rss201rev2Feed
