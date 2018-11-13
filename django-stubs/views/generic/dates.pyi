import datetime
from typing import Any, Dict, Optional, Sequence, Tuple, Type

from django.db import models
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

class YearMixin:
    year_format = ...  # type: str
    year = ...  # type: Optional[str]
    kwargs = ...  # type: Dict[str, object]
    request = ...  # type: HttpRequest
    def get_year_format(self) -> str: ...
    def get_year(self) -> str: ...
    def get_next_year(self, date: datetime.date) -> Optional[datetime.date]: ...
    def get_previous_year(self, date: datetime.date) -> Optional[datetime.date]: ...

class MonthMixin:
    month_format = ...  # type: str
    month = ...  # type: Optional[str]
    request = ...  # type: HttpRequest
    kwargs = ...  # type: Dict[str, object]
    def get_month_format(self) -> str: ...
    def get_month(self) -> str: ...
    def get_next_month(self, date: datetime.date) -> Optional[datetime.date]: ...
    def get_previous_month(self, date: datetime.date) -> Optional[datetime.date]: ...

class DayMixin:
    day_format = ...  # type: str
    day = ...  # type: Optional[str]
    request = ...  # type: HttpRequest
    kwargs = ...  # type: Dict[str, object]
    def get_day_format(self) -> str: ...
    def get_day(self) -> str: ...
    def get_next_day(self, date: datetime.date) -> Optional[datetime.date]: ...
    def get_previous_day(self, date: datetime.date) -> Optional[datetime.date]: ...

class WeekMixin:
    week_format = ...  # type: str
    week = ...  # type: Optional[str]
    request = ...  # type: HttpRequest
    kwargs = ...  # type: Dict[str, object]
    def get_week_format(self) -> str: ...
    def get_week(self) -> str: ...
    def get_next_week(self, date: datetime.date) -> Optional[datetime.date]: ...
    def get_previous_week(self, date: datetime.date) -> Optional[datetime.date]: ...

class DateMixin:
    date_field = ...  # type: Optional[str]
    allow_future = ...  # type: bool
    model = ...  # type: Optional[Type[models.Model]]
    def get_date_field(self) -> str: ...
    def get_allow_future(self) -> bool: ...
    def uses_datetime_field(self) -> bool: ...

DatedItems = Tuple[Optional[Sequence[datetime.date]], Sequence[object], Dict[str, Any]]

class BaseDateListView(MultipleObjectMixin, DateMixin, View):
    allow_empty = ...  # type: bool
    date_list_period = ...  # type: str
    def render_to_response(self, context: Dict[str, object], **response_kwargs: object) -> HttpResponse: ...
    def get(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse: ...
    def get_dated_items(self) -> DatedItems: ...
    def get_ordering(self) -> Sequence[str]: ...
    def get_dated_queryset(self, **lookup: object) -> models.query.QuerySet: ...
    def get_date_list_period(self) -> str: ...
    def get_date_list(self, queryset: models.query.QuerySet, date_type: str = None, ordering: str = ...) -> models.query.QuerySet: ...

class BaseArchiveIndexView(BaseDateListView):
    context_object_name = ...  # type: str
    def get_dated_items(self) -> DatedItems: ...

class ArchiveIndexView(MultipleObjectTemplateResponseMixin, BaseArchiveIndexView):
    template_name_suffix = ...  # type: str

class BaseYearArchiveView(YearMixin, BaseDateListView):
    date_list_period = ...  # type: str
    make_object_list = ...  # type: bool
    def get_dated_items(self) -> DatedItems: ...
    def get_make_object_list(self) -> bool: ...

class YearArchiveView(MultipleObjectTemplateResponseMixin, BaseYearArchiveView):
    template_name_suffix = ...  # type: str

class BaseMonthArchiveView(YearMixin, MonthMixin, BaseDateListView):
    date_list_period = ...  # type: str
    def get_dated_items(self) -> DatedItems: ...

class MonthArchiveView(MultipleObjectTemplateResponseMixin, BaseMonthArchiveView):
    template_name_suffix = ...  # type: str

class BaseWeekArchiveView(YearMixin, WeekMixin, BaseDateListView):
    def get_dated_items(self) -> DatedItems: ...

class WeekArchiveView(MultipleObjectTemplateResponseMixin, BaseWeekArchiveView):
    template_name_suffix = ...  # type: str

class BaseDayArchiveView(YearMixin, MonthMixin, DayMixin, BaseDateListView):
    def get_dated_items(self) -> DatedItems: ...

class DayArchiveView(MultipleObjectTemplateResponseMixin, BaseDayArchiveView):
    template_name_suffix = ...  # type: str

class BaseTodayArchiveView(BaseDayArchiveView):
    def get_dated_items(self) -> DatedItems: ...

class TodayArchiveView(MultipleObjectTemplateResponseMixin, BaseTodayArchiveView):
    template_name_suffix = ...  # type: str

class BaseDateDetailView(YearMixin, MonthMixin, DayMixin, DateMixin, BaseDetailView):
    def get_object(self, queryset: models.query.QuerySet=None) -> models.Model: ...

class DateDetailView(SingleObjectTemplateResponseMixin, BaseDateDetailView):
    template_name_suffix = ...  # type: str

def timezone_today() -> datetime.date: ...
