from typing import Any

from django.contrib import admin

class FlatPageAdmin(admin.ModelAdmin):
    form: Any
    fieldsets: Any
    list_display: Any
    list_filter: Any
    search_fields: Any
