from __future__ import annotations

from typing import assert_type

from django.core.handlers.wsgi import WSGIRequest
from django.test.client import Client
from django.test.testcases import TestCase, _AssertTemplateNotUsedContext, _AssertTemplateUsedContext


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
        with self.assertTemplateUsed("template.html") as ctx:
            assert_type(ctx, _AssertTemplateUsedContext)
        with self.assertTemplateUsed(template_name="template.html") as ctx:
            assert_type(ctx, _AssertTemplateUsedContext)

    def test_assert_template_not_used(self) -> None:
        response = self.client.get("/url")
        assert_type(self.assertTemplateNotUsed(response, "template.html"), None)
        with self.assertTemplateNotUsed("template.html") as ctx:
            assert_type(ctx, _AssertTemplateNotUsedContext)
        with self.assertTemplateNotUsed(template_name="template.html") as ctx:
            assert_type(ctx, _AssertTemplateNotUsedContext)
