from __future__ import annotations

from django.template.response import TemplateResponse
from django.test import RequestFactory
from django.views.generic import TemplateView
from typing_extensions import assert_type


class MyTemplateView(TemplateView):
    template_name = "template.html"


request = RequestFactory().get("/")
response = MyTemplateView.as_view()(request)
assert_type(response, TemplateResponse)
assert_type(response.rendered_content, str)
