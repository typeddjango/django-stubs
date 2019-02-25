import collections
import datetime
from typing import Any, Dict, Iterator, List, Optional, Union, Type

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.forms.utils import ErrorList
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict

from django import forms

UserModel: Any

class ReadOnlyPasswordHashWidget(forms.Widget):
    attrs: Dict[Any, Any]
    template_name: str = ...

class ReadOnlyPasswordHashField(forms.Field):
    widget: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def bound_data(self, data: None, initial: str) -> str: ...
    def has_changed(self, initial: str, data: Optional[str]) -> bool: ...

class UsernameField(forms.CharField):
    def to_python(self, value: Optional[str]) -> str: ...

class UserCreationForm(forms.ModelForm):
    auto_id: str
    data: Dict[str, str]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    instance: User
    is_bound: bool
    label_suffix: str
    error_messages: Any = ...
    password1: Any = ...
    password2: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def clean_password2(self) -> str: ...

class UserChangeForm(forms.ModelForm):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[str, Optional[Union[List[Any], datetime.datetime, int, str]]]
    instance: User
    is_bound: bool
    label_suffix: str
    password: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def clean_password(self) -> str: ...

class AuthenticationForm(forms.Form):
    auto_id: str
    data: QueryDict
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: MultiValueDict
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    username: Any = ...
    password: Any = ...
    error_messages: Any = ...
    request: WSGIRequest = ...
    user_cache: None = ...
    username_field: Any = ...
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None: ...
    def confirm_login_allowed(self, user: AbstractBaseUser) -> None: ...
    def get_user(self) -> User: ...
    def get_invalid_login_error(self) -> ValidationError: ...

class PasswordResetForm(forms.Form):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    email: Any = ...
    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: Dict[str, Union[AbstractBaseUser, str]],
        from_email: Optional[str],
        to_email: str,
        html_email_template_name: Optional[str] = ...,
    ) -> None: ...
    def get_users(self, email: str) -> Iterator[Any]: ...
    def save(
        self,
        domain_override: Optional[str] = ...,
        subject_template_name: str = ...,
        email_template_name: str = ...,
        use_https: bool = ...,
        token_generator: PasswordResetTokenGenerator = ...,
        from_email: Optional[str] = ...,
        request: Optional[WSGIRequest] = ...,
        html_email_template_name: Optional[str] = ...,
        extra_email_context: Optional[Dict[str, str]] = ...,
    ) -> None: ...

class SetPasswordForm(forms.Form):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    error_messages: Any = ...
    new_password1: Any = ...
    new_password2: Any = ...
    user: User = ...
    def __init__(self, user: Optional[AbstractBaseUser], *args: Any, **kwargs: Any) -> None: ...
    def clean_new_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> AbstractBaseUser: ...

class PasswordChangeForm(SetPasswordForm):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    user: User
    error_messages: Any = ...
    old_password: Any = ...
    field_order: Any = ...
    def clean_old_password(self) -> str: ...

class AdminPasswordChangeForm(forms.Form):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    error_messages: Any = ...
    required_css_class: str = ...
    password1: Any = ...
    password2: Any = ...
    user: User = ...
    def __init__(self, user: AbstractUser, *args: Any, **kwargs: Any) -> None: ...
    def clean_password2(self) -> str: ...
    def save(self, commit: bool = ...) -> AbstractUser: ...
    @property
    def changed_data(self) -> List[str]: ...
