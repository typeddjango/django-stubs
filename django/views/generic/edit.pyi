from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.forms.forms import (
    BaseForm,
    Form,
)
from django.forms.models import ModelForm
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDict
from typing import (
    Any,
    Dict,
    Optional,
    Type,
    Union,
)


class BaseCreateView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class BaseUpdateView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class DeletionMixin:
    def delete(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect: ...
    def get_success_url(self) -> str: ...
    def post(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect: ...


class FormMixin:
    def form_invalid(self, form: Form) -> TemplateResponse: ...
    def form_valid(self, form: Form) -> HttpResponseRedirect: ...
    def get_context_data(self, **kwargs) -> Dict[str, Any]: ...
    def get_form(self, form_class: None = ...) -> BaseForm: ...
    def get_form_class(self) -> Any: ...
    def get_form_kwargs(self) -> Dict[str, Union[None, MultiValueDict]]: ...
    def get_initial(self) -> Dict[Any, Any]: ...
    def get_prefix(self) -> None: ...
    def get_success_url(self) -> str: ...


class ModelFormMixin:
    def get_form_class(self) -> Type[ModelForm]: ...
    def get_form_kwargs(
        self
    ) -> Dict[str, Union[None, MultiValueDict, Model]]: ...
    def get_success_url(self) -> str: ...


class ProcessFormView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...
    def post(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> Union[TemplateResponse, HttpResponseRedirect]: ...