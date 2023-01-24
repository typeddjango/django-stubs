from typing import Any

from django.contrib import admin
from django.db.models import Model

class SiteAdmin(admin.ModelAdmin[Model]):
    list_display: Any
    search_fields: Any
