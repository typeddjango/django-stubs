from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseBase, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.test import RequestFactory
from django.views.generic import TemplateView
from typing_extensions import assert_type, override

request = RequestFactory().get("/")


class BareTemplateView(TemplateView):
    template_name = "template.html"


class NarrowedTemplateView(TemplateView[TemplateResponse]):
    template_name = "template.html"


def bare_is_permissive(view: BareTemplateView) -> None:
    assert_type(BareTemplateView.as_view()(request), HttpResponse)
    assert_type(view.get(request), HttpResponse)
    assert_type(view.render_to_response({}), HttpResponse)


def parametrising_narrows_the_response(view: NarrowedTemplateView) -> None:
    response = NarrowedTemplateView.as_view()(request)
    assert_type(response, TemplateResponse)
    assert_type(response.rendered_content, str)
    assert_type(view.get(request), TemplateResponse)
    assert_type(view.render_to_response({}), TemplateResponse)


def dispatch_is_never_narrowed(view: NarrowedTemplateView) -> None:
    assert_type(view.dispatch(request), HttpResponseBase)
    assert_type(view.http_method_not_allowed(request), HttpResponse)
    assert_type(view.options(request), HttpResponseBase)


class LoginRequired(LoginRequiredMixin, TemplateView):
    template_name = "template.html"


class PermissionRequired(PermissionRequiredMixin, NarrowedTemplateView):
    template_name = "template.html"
    permission_required = "app.some_permission"


class UserPassesTest(UserPassesTestMixin, TemplateView):
    template_name = "template.html"

    @override
    def test_func(self) -> bool:
        return True


class RedirectingGet(TemplateView):
    template_name = "template.html"

    @override
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_anonymous:
            return redirect("/login/")
        return super().get(request, *args, **kwargs)


class UnionGet(TemplateView):
    template_name = "template.html"

    @override
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | JsonResponse:
        return JsonResponse({})


class WideningDispatch(TemplateView):
    template_name = "template.html"

    @override
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        return super().dispatch(request, *args, **kwargs)
