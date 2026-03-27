from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from typing_extensions import TypedDict, assert_type

# render function arguments
TestContext = TypedDict("TestContext", {"user": Any})
test_context: TestContext = {"user": "test"}
assert_type(render(HttpRequest(), "", test_context), HttpResponse)

# redirect return annotation
assert_type(redirect(to="", permanent=True), HttpResponsePermanentRedirect)
assert_type(redirect(to="", permanent=False), HttpResponseRedirect)
assert_type(redirect(to=""), HttpResponseRedirect)

var: bool = True
assert_type(redirect(to="", permanent=var), HttpResponseRedirect | HttpResponsePermanentRedirect)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
