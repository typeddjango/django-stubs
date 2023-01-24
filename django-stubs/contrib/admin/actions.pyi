from django.contrib.admin.options import ModelAdmin
from django.db.models import Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.template.response import TemplateResponse

def delete_selected(
    modeladmin: ModelAdmin[Model], request: HttpRequest, queryset: QuerySet[Model]
) -> TemplateResponse | None: ...
