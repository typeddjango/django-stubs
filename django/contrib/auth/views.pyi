from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDict
from typing import (
    Any,
    Dict,
    Optional,
    Set,
    Union,
)


def redirect_to_login(
    next: str,
    login_url: Optional[str] = ...,
    redirect_field_name: Optional[str] = ...
) -> HttpResponseRedirect: ...


class LoginView:
    def dispatch(
        self,
        request: HttpRequest,
        *args,
        **kwargs
    ) -> Union[HttpResponseRedirect, TemplateResponse]: ...
    def form_valid(
        self,
        form: AuthenticationForm
    ) -> HttpResponseRedirect: ...
    def get_context_data(self, **kwargs) -> Dict[str, Any]: ...
    def get_form_class(self) -> Any: ...
    def get_form_kwargs(
        self
    ) -> Dict[str, Union[None, MultiValueDict, WSGIRequest]]: ...
    def get_redirect_url(self) -> str: ...
    def get_success_url(self) -> str: ...


class LogoutView:
    def dispatch(
        self,
        request: HttpRequest,
        *args,
        **kwargs
    ) -> Union[HttpResponseRedirect, TemplateResponse]: ...
    def get_next_page(self) -> Optional[str]: ...
    def post(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class PasswordChangeDoneView:
    def dispatch(self, *args, **kwargs) -> TemplateResponse: ...


class PasswordChangeView:
    def dispatch(
        self,
        *args,
        **kwargs
    ) -> Union[HttpResponseRedirect, TemplateResponse]: ...
    def form_valid(
        self,
        form: PasswordChangeForm
    ) -> HttpResponseRedirect: ...
    def get_form_kwargs(
        self
    ) -> Dict[str, Union[None, User, MultiValueDict]]: ...


class PasswordResetConfirmView:
    def dispatch(
        self,
        *args,
        **kwargs
    ) -> Union[HttpResponseRedirect, TemplateResponse]: ...
    def form_valid(self, form: SetPasswordForm) -> HttpResponseRedirect: ...
    def get_form_kwargs(
        self
    ) -> Dict[str, Union[None, User, MultiValueDict]]: ...
    def get_user(self, uidb64: str) -> Optional[User]: ...


class PasswordResetView:
    def dispatch(
        self,
        *args,
        **kwargs
    ) -> Union[HttpResponseRedirect, TemplateResponse]: ...
    def form_valid(self, form: PasswordResetForm) -> HttpResponseRedirect: ...


class SuccessURLAllowedHostsMixin:
    def get_success_url_allowed_hosts(self) -> Set[str]: ...