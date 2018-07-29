from datetime import datetime
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.query import QuerySet
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


def _get_sitemap_full_url(sitemap_url: None): ...


def ping_google(sitemap_url: None = ..., ping_url: str = ...) -> None: ...


class GenericSitemap:
    def __init__(
        self,
        info_dict: Dict[str, Union[QuerySet, datetime]],
        priority: Optional[float] = ...,
        changefreq: Optional[str] = ...,
        protocol: Optional[str] = ...
    ) -> None: ...
    def lastmod(self, item: Model) -> None: ...


class Sitemap:
    def _urls(
        self,
        page: Union[str, int],
        protocol: str,
        domain: str
    ) -> Union[List[Dict[str, Union[Model, str, None]]], List[Dict[str, object]]]: ...
    def get_urls(
        self,
        page: Union[str, int] = ...,
        site: Optional[Union[RequestSite, Site]] = ...,
        protocol: Optional[str] = ...
    ) -> Union[List[Dict[str, Union[Model, str, datetime, None]]], List[Dict[str, object]]]: ...
    def items(self) -> List[Any]: ...
    def location(self, obj: Model) -> str: ...
    @property
    def paginator(self) -> Paginator: ...