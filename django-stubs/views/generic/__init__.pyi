from django.views.generic.base import RedirectView as RedirectView, TemplateView as TemplateView, View as View
from django.views.generic.dates import ArchiveIndexView as ArchiveIndexView, DateDetailView as DateDetailView, DayArchiveView as DayArchiveView, MonthArchiveView as MonthArchiveView, TodayArchiveView as TodayArchiveView, WeekArchiveView as WeekArchiveView, YearArchiveView as YearArchiveView
from django.views.generic.detail import DetailView as DetailView
from django.views.generic.edit import CreateView as CreateView, DeleteView as DeleteView, FormView as FormView, UpdateView as UpdateView
from django.views.generic.list import ListView as ListView

class GenericViewError(Exception): ...
