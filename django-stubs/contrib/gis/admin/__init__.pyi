from django.contrib.admin import (
    AdminSite as AdminSite,
    HORIZONTAL as HORIZONTAL,
    ModelAdmin as ModelAdmin,
    StackedInline as StackedInline,
    TabularInline as TabularInline,
    VERTICAL as VERTICAL,
    autodiscover as autodiscover,
    register as register,
    site as site,
)
from django.contrib.gis.admin.options import GeoModelAdmin as GeoModelAdmin, OSMGeoAdmin as OSMGeoAdmin
