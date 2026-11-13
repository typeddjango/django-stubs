from __future__ import annotations

from typing import Any, assert_type

from django import views
from django.db import models
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from typing_extensions import TypedDict


class Animal(models.Model):
    def get_absolute_url(self) -> str:
        raise NotImplementedError


class Scenery(views.View): ...


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

# redirect supports reverse_lazy
assert_type(redirect(to=reverse_lazy("")), HttpResponseRedirect)

# redirect supports get_absolute_url()
assert_type(redirect(to=Animal()), HttpResponseRedirect)

# redirect supports view classes
assert_type(redirect(to=Scenery.as_view()), HttpResponseRedirect)

# resolve_url supports reverse_lazy
assert_type(resolve_url(to=reverse_lazy("")), str)

# resolve_url supports get_absolute_url()
assert_type(resolve_url(to=Animal()), str)

# resolve_url supports view classes
assert_type(resolve_url(to=Scenery.as_view()), str)
