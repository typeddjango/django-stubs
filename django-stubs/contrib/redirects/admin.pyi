from typing import Any

from django.contrib import admin
from django.db.models import Model

class RedirectAdmin(admin.ModelAdmin[Model]):
    list_display: Any
    list_filter: Any
    search_fields: Any
    radio_fields: Any
