from typing import Any

from django.contrib import admin
from django.db.models import Model

class FlatPageAdmin(admin.ModelAdmin[Model]):
    form: Any
    fieldsets: Any
    list_display: Any
    list_filter: Any
    search_fields: Any
