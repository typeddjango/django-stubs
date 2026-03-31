from __future__ import annotations

from typing import Any

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from django.template.base import Template
from django.test.client import AsyncClient, AsyncRequestFactory, Client, RequestFactory
from django.test.utils import ContextList
from typing_extensions import assert_type

# Client response attributes
client = Client()
response = client.get("foo")
assert_type(response.wsgi_request, WSGIRequest)
assert_type(response.request, dict[str, Any])
assert_type(response.templates, list[Template])
assert_type(response.client, Client)
assert_type(response.context, ContextList | dict[str, Any])
assert_type(response.context_data, dict[str, Any] | None)
assert_type(response.content, bytes)
assert_type(response.redirect_chain, list[tuple[str, int]])
assert_type(response.text, str)
response.json()


# Async client response attributes
async def test_async_client() -> None:
    async_client = AsyncClient()
    response = await async_client.get("foo")
    assert_type(response.asgi_request, ASGIRequest)
    assert_type(response.request, dict[str, Any])
    assert_type(response.templates, list[Template])
    assert_type(response.client, AsyncClient)
    assert_type(response.context, ContextList | dict[str, Any])
    assert_type(response.context_data, dict[str, Any] | None)
    assert_type(response.content, bytes)
    assert_type(response.redirect_chain, list[tuple[str, int]])
    response.json()


# Request factories
factory = RequestFactory()
assert_type(factory.get("foo"), WSGIRequest)

async_factory = AsyncRequestFactory()
assert_type(async_factory.get("foo"), ASGIRequest)
