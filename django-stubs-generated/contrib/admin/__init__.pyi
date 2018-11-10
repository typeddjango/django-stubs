from typing import Optional

from django.contrib.admin.decorators import register as register
from django.contrib.admin.filters import \
    AllValuesFieldListFilter as AllValuesFieldListFilter
from django.contrib.admin.filters import \
    BooleanFieldListFilter as BooleanFieldListFilter
from django.contrib.admin.filters import \
    ChoicesFieldListFilter as ChoicesFieldListFilter
from django.contrib.admin.filters import \
    DateFieldListFilter as DateFieldListFilter
from django.contrib.admin.filters import FieldListFilter as FieldListFilter
from django.contrib.admin.filters import ListFilter as ListFilter
from django.contrib.admin.filters import \
    RelatedFieldListFilter as RelatedFieldListFilter
from django.contrib.admin.filters import \
    RelatedOnlyFieldListFilter as RelatedOnlyFieldListFilter
from django.contrib.admin.filters import SimpleListFilter as SimpleListFilter
from django.contrib.admin.helpers import \
    ACTION_CHECKBOX_NAME as ACTION_CHECKBOX_NAME
from django.contrib.admin.options import HORIZONTAL as HORIZONTAL
from django.contrib.admin.options import VERTICAL as VERTICAL
from django.contrib.admin.options import ModelAdmin as ModelAdmin
from django.contrib.admin.options import StackedInline as StackedInline
from django.contrib.admin.options import TabularInline as TabularInline
from django.contrib.admin.sites import AdminSite as AdminSite
from django.contrib.admin.sites import site as site


def autodiscover() -> None: ...
