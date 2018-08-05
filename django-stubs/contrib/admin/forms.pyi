from typing import Any, Optional

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User


class AdminAuthenticationForm(AuthenticationForm):
    auto_id: str
    data: Dict[str, str]
    empty_permitted: bool
    error_class: Type[django.forms.utils.ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    request: None
    user_cache: None
    error_messages: Any = ...
    required_css_class: str = ...
    def confirm_login_allowed(self, user: User) -> None: ...

class AdminPasswordChangeForm(PasswordChangeForm):
    auto_id: str
    data: Dict[Any, Any]
    empty_permitted: bool
    error_class: Type[django.forms.utils.ErrorList]
    fields: collections.OrderedDict
    files: Dict[Any, Any]
    initial: Dict[Any, Any]
    is_bound: bool
    label_suffix: str
    user: django.utils.functional.SimpleLazyObject
    required_css_class: str = ...
