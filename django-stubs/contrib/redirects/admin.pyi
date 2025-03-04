from typing import Any, ClassVar

from django.contrib import admin

class RedirectAdmin(admin.ModelAdmin):
    list_display: Any
    list_filter: Any
    search_fields: Any
    radio_fields: ClassVar[Any]
