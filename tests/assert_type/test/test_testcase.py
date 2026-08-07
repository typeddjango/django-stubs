from __future__ import annotations

from django.core.handlers.wsgi import WSGIRequest
from django.test.client import Client
from django.test.testcases import TestCase, _AssertTemplateNotUsedContext, _AssertTemplateUsedContext
from typing_extensions import assert_type


class ExampleTestCase(TestCase):
    def test_method(self) -> None:
        assert_type(self.client, Client)
        resp = self.client.post("/url", {"doit": "srs"}, "application/json", False, True, extra="value")
        assert_type(resp.status_code, int)
        resp.json()
        assert_type(resp.wsgi_request, WSGIRequest)

    def test_assert_template_used(self) -> None:
        response = self.client.get("/url")
        assert_type(self.assertTemplateUsed(response, "template.html"), None)
        assert_type(self.assertTemplateUsed("template.html"), _AssertTemplateUsedContext)
        assert_type(self.assertTemplateUsed(template_name="template.html"), _AssertTemplateUsedContext)

    def test_assert_template_not_used(self) -> None:
        response = self.client.get("/url")
        assert_type(self.assertTemplateNotUsed(response, "template.html"), None)
        assert_type(self.assertTemplateNotUsed("template.html"), _AssertTemplateNotUsedContext)
        assert_type(self.assertTemplateNotUsed(template_name="template.html"), _AssertTemplateNotUsedContext)
