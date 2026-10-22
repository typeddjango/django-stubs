from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

if TYPE_CHECKING:
    from django.http.request import HttpRequest


@staff_member_required
def bare(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


@staff_member_required(redirect_field_name="next", login_url="/login/")
def configured(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def views(request: HttpRequest) -> None:
    assert_type(bare(request), HttpResponse)
    assert_type(configured(request), HttpResponse)
