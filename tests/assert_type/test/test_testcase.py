from __future__ import annotations

from typing import assert_type

from django.core.handlers.wsgi import WSGIRequest
from django.test.client import Client
from django.test.testcases import TestCase


class ExampleTestCase(TestCase):
    def test_method(self) -> None:
        assert_type(self.client, Client)
        resp = self.client.post("/url", {"doit": "srs"}, "application/json", False, True, extra="value")
        assert_type(resp.status_code, int)
        resp.json()
        assert_type(resp.wsgi_request, WSGIRequest)
