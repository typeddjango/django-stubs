from typing import Any, TypeVar

from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group
from django.http.request import HttpRequest
from django.http.response import HttpResponse

csrf_protect_m: Any
sensitive_post_parameters_m: Any
_M = TypeVar("_M", bound=AbstractUser)

class GroupAdmin(admin.ModelAdmin[Group]): ...

class UserAdmin(admin.ModelAdmin[_M]):
    change_user_password_template: Any
    add_fieldsets: Any
    add_form: Any
    change_password_form: Any
    def user_change_password(self, request: HttpRequest, id: str, form_url: str = ...) -> HttpResponse: ...
