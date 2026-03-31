from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING

from django.http.response import HttpResponse, StreamingHttpResponse
from django.utils.translation import gettext_lazy as _
from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.http.request import HttpRequest

# HttpResponse with various content types


def empty_response(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def str_response(request: HttpRequest) -> HttpResponse:
    return HttpResponse("It works!")


def bytes_response(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b"It works!")


def object_response(request: HttpRequest) -> HttpResponse:
    return HttpResponse(_("It works!"))


# HttpResponse.content is always bytes
response = HttpResponse()
assert_type(response.content, bytes)
response.content = "It works!"
assert_type(response.content, bytes)
response.content = b"It works!"
assert_type(response.content, bytes)
response.content = _("It works!")
assert_type(response.content, bytes)
assert_type(response.text, str)

# StreamingHttpResponse with various content types


def empty_streaming(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse()


def str_streaming(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse(["It works!"])


def bytes_streaming(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse([b"It works!"])


def object_streaming(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse([_("It works!")])


def mixed_streaming(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse([_("Yes"), "/", _("No")])


# StreamingHttpResponse.streaming_content after various assignments
streaming_response = StreamingHttpResponse()
assert_type(streaming_response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])
streaming_response.streaming_content = ["It works!"]
assert_type(streaming_response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])
streaming_response.streaming_content = [b"It works!"]
assert_type(streaming_response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])
streaming_response.streaming_content = [_("It works!")]
assert_type(streaming_response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])
streaming_response.streaming_content = [_("Yes"), "/", _("No")]
assert_type(streaming_response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])


# Async streaming constructors
def async_str_response(request: HttpRequest) -> StreamingHttpResponse:
    async def str_iterator() -> AsyncIterator[str]:
        yield "It works!"

    return StreamingHttpResponse(str_iterator())


def async_bytes_response(request: HttpRequest) -> StreamingHttpResponse:
    async def bytes_iterator() -> AsyncIterator[bytes]:
        yield b"It works!"

    return StreamingHttpResponse(bytes_iterator())


def async_object_response(request: HttpRequest) -> StreamingHttpResponse:
    async def object_iterator() -> AsyncIterator[object]:
        yield _("It works!")

    return StreamingHttpResponse(object_iterator())


def async_mixed_response(request: HttpRequest) -> StreamingHttpResponse:
    async def mixed_iterator() -> AsyncIterator[object]:
        yield _("Yes")
        yield "/"
        yield _("No")

    return StreamingHttpResponse(mixed_iterator())


# Async streaming_content assignment
def async_streaming_content_str() -> None:
    response = StreamingHttpResponse()

    async def str_iterator() -> AsyncIterator[str]:
        yield "It works!"

    response.streaming_content = str_iterator()
    assert_type(response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])


def async_streaming_content_bytes() -> None:
    response = StreamingHttpResponse()

    async def bytes_iterator() -> AsyncIterator[bytes]:
        yield b"It works!"

    response.streaming_content = bytes_iterator()
    assert_type(response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])  # type: ignore[assert-type]  # mypy narrows to AsyncIterator[bytes]


def async_streaming_content_object() -> None:
    response = StreamingHttpResponse()

    async def object_iterator() -> AsyncIterator[object]:
        yield _("It works!")

    response.streaming_content = object_iterator()
    assert_type(response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])


def async_streaming_content_mixed() -> None:
    response = StreamingHttpResponse()

    async def mixed_iterator() -> AsyncIterator[object]:
        yield _("Yes")
        yield "/"
        yield _("No")

    response.streaming_content = mixed_iterator()
    assert_type(response.streaming_content, Iterator[bytes] | AsyncIterator[bytes])
