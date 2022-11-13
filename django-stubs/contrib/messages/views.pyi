from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.utils.functional import _StrOrPromise

class SuccessMessageMixin:
    success_message: _StrOrPromise
    def form_valid(self, form: BaseForm) -> HttpResponse: ...
    def get_success_message(self, cleaned_data: dict[str, str]) -> _StrOrPromise: ...
