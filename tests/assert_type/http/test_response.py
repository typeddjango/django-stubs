from collections.abc import AsyncIterable, AsyncIterator, Iterable

from django.http.response import HttpResponse, StreamingHttpResponse
from typing_extensions import assert_type

# HttpResponse
# ============

response = HttpResponse()
response.content = "abc"
assert_type(response.content, bytes)

# StreamingHttpResponse
# =====================

streaming_response = StreamingHttpResponse()

# We can assign `Iterator`s ...
streaming_response.streaming_content = iter([1, 2])


async def async_iterator() -> AsyncIterator[int]:
    yield 1


streaming_response.streaming_content = async_iterator()

# ... but only get `Iterable` back:
assert_type(streaming_response.streaming_content, Iterable[object] | AsyncIterable[object])
