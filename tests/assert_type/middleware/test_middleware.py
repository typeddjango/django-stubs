from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.redirects.middleware import RedirectFallbackMiddleware
from django.http.response import (
    FileResponse,
    HttpResponse,
    HttpResponseGone,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    HttpResponseRedirectBase,
)
from django.middleware.common import CommonMiddleware
from django.middleware.locale import LocaleMiddleware
from typing_extensions import override

if TYPE_CHECKING:
    from django.http.request import HttpRequest


class CustomCommonMiddleware(CommonMiddleware):
    response_redirect_class = HttpResponsePermanentRedirect


class BrokenCustomCommonMiddleware(CommonMiddleware):
    response_redirect_class = FileResponse  # type:ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class CustomLocaleMiddleware(LocaleMiddleware):
    response_redirect_class = HttpResponseRedirect


class BrokenCustomLocaleMiddleware(CommonMiddleware):
    response_redirect_class = FileResponse  # type:ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class CustomRedirectFallbackMiddleware(RedirectFallbackMiddleware):
    response_redirect_class = HttpResponseRedirect
    response_gone_class = HttpResponseGone


class CustomRedirectFallbackMiddleware2(RedirectFallbackMiddleware):
    response_redirect_class = HttpResponseRedirectBase
    response_gone_class = HttpResponse


class BrokenCustomRedirectFallbackMiddleware(RedirectFallbackMiddleware):
    response_redirect_class = HttpResponse  # type:ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]
    response_gone_class = 12  # type:ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]


class ResponseGoneFallbackMiddleware(RedirectFallbackMiddleware):
    @override
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        return self.response_gone_class()
