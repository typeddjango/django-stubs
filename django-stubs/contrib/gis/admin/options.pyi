from typing import Any, ClassVar

from django.contrib.admin import ModelAdmin
from django.contrib.gis.forms import OSMWidget
from django.db.models import Field
from django.forms.fields import Field as FormField
from django.http import HttpRequest

class GeoModelAdminMixin:
    gis_widget: ClassVar[type[OSMWidget]]
    gis_widget_kwargs: ClassVar[dict[str, Any]]
    def formfield_for_dbfield(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> FormField: ...

class GISModelAdmin(GeoModelAdminMixin, ModelAdmin): ...
