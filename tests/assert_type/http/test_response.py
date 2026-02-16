from collections.abc import AsyncIterable, AsyncIterator, Iterator

from django.http.response import HttpResponse, StreamingHttpResponse
from typing_extensions import assert_type

# HttpResponse
# ============

response = HttpResponse()
# We can assign any objects, but get bytes back:
response.content = "abc"
assert_type(response.content, bytes)

# StreamingHttpResponse
# =====================

streaming_response = StreamingHttpResponse()

# We can assign any `Iterable`s ...
streaming_response.streaming_content = [1, 2]
streaming_response.streaming_content = iter(["a", "b"])


def async_iterable() -> AsyncIterable[int]:
    raise NotImplementedError


streaming_response.streaming_content = async_iterable()

# ... but get `Iterator` back:
assert_type(streaming_response.streaming_content, Iterator[object] | AsyncIterator[object])
