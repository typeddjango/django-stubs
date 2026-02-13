from typing import Any

from django.contrib import admin
from django.contrib.auth.models import Group, _UserType
from django.http.request import HttpRequest
from django.http.response import HttpResponse

class GroupAdmin(admin.ModelAdmin[Group]): ...

class UserAdmin(admin.ModelAdmin[_UserType]):
    change_user_password_template: Any
    add_fieldsets: Any
    add_form: Any
    change_password_form: Any
    def lookup_allowed(self, lookup: str, value: str, request: HttpRequest) -> bool: ...
    def user_change_password(self, request: HttpRequest, id: str, form_url: str = ...) -> HttpResponse: ...
