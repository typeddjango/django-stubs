from collections.abc import Iterable
from logging import Logger
from typing import Any, Generic

from django import forms
from django.contrib.auth.models import _User, _UserType
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import _ErrorMessagesDict
from django.forms.fields import _ClassLevelWidgetT
from django.forms.widgets import Widget
from django.http.request import HttpRequest
from typing_extensions import TypeAlias

logger: Logger

UserModel: TypeAlias = type[_User]

class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name: str
    read_only: bool
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]: ...

class ReadOnlyPasswordHashField(forms.Field):
    widget: _ClassLevelWidgetT
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class UsernameField(forms.CharField):
    def to_python(self, value: Any | None) -> Any | None: ...
    def widget_attrs(self, widget: Widget) -> dict[str, Any]: ...

# mypy is incorrectly interpreting this as not generic, so explicitly say it is
class BaseUserCreationForm(Generic[_UserType], forms.ModelForm[_UserType]):
    error_messages: _ErrorMessagesDict
    password1: forms.Field
    password2: forms.Field
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def clean_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> _UserType: ...

class UserCreationForm(BaseUserCreationForm[_UserType]):
    def clean_username(self) -> str: ...

class UserChangeForm(forms.ModelForm[_UserType]):
    password: forms.Field
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class AuthenticationForm(forms.Form):
    username: forms.Field
    password: forms.Field
    error_messages: _ErrorMessagesDict
    request: HttpRequest | None
    user_cache: _User | None
    username_field: models.Field
    def __init__(self, request: HttpRequest | None = ..., *args: Any, **kwargs: Any) -> None: ...
    def confirm_login_allowed(self, user: _User) -> None: ...
    def get_user(self) -> _User: ...
    def get_invalid_login_error(self) -> ValidationError: ...
    def clean(self) -> dict[str, Any]: ...

class PasswordResetForm(forms.Form):
    email: forms.Field
    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = ...,
    ) -> None: ...
    def get_users(self, email: str) -> Iterable[_User]: ...
    def save(
        self,
        domain_override: str | None = ...,
        subject_template_name: str = ...,
        email_template_name: str = ...,
        use_https: bool = ...,
        token_generator: PasswordResetTokenGenerator = ...,
        from_email: str | None = ...,
        request: HttpRequest | None = ...,
        html_email_template_name: str | None = ...,
        extra_email_context: dict[str, str] | None = ...,
    ) -> None: ...

class SetPasswordForm(Generic[_UserType], forms.Form):
    error_messages: _ErrorMessagesDict
    new_password1: forms.Field
    new_password2: forms.Field
    user: _UserType
    def __init__(self, user: _UserType, *args: Any, **kwargs: Any) -> None: ...
    def clean_new_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> _UserType: ...

class PasswordChangeForm(SetPasswordForm):
    error_messages: _ErrorMessagesDict
    old_password: forms.Field
    def clean_old_password(self) -> str: ...

class AdminPasswordChangeForm(Generic[_UserType], forms.Form):
    error_messages: _ErrorMessagesDict
    required_css_class: str
    password1: forms.Field
    password2: forms.Field
    user: _UserType
    def __init__(self, user: _UserType, *args: Any, **kwargs: Any) -> None: ...
    def clean_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> _UserType: ...
    @property
    def changed_data(self) -> list[str]: ...
