from django.http import HttpRequest
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.utils.functional import _StrPromise
from django.utils.safestring import SafeString
from typing_extensions import assert_type

request = HttpRequest()

input_result = csrf_input_lazy(request)
assert_type(input_result, SafeString)

token_result = csrf_token_lazy(request)
assert_type(token_result, _StrPromise)
