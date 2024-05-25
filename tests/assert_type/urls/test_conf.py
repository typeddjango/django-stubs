from typing import List, Tuple

from django.conf.urls.i18n import urlpatterns as i18n_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.flatpages import urls as flatpages_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import URLPattern, URLResolver, _AnyURL, include, path, re_path
from django.utils.translation import gettext_lazy as _
from typing_extensions import assert_type

# Test 'path' accepts mix of pattern and resolver object
include1: Tuple[List[_AnyURL], None, None] = ([], None, None)
assert_type(path("test/", include1), URLResolver)

# Test 'path' accepts pattern resolver union subset
include2: Tuple[List[URLPattern], None, None] = ([], None, None)
assert_type(path("test/", include2), URLResolver)

# Test 'path'
assert_type(path("admin/", admin.site.urls), URLResolver)
assert_type(path(_("admin/"), admin.site.urls, name="admin"), URLResolver)
assert_type(path("login/", LoginView.as_view(), name="login1"), URLPattern)
assert_type(path(_("login/"), LoginView.as_view(), name="login2"), URLPattern)


def v1() -> HttpResponse: ...
async def v2() -> HttpResponse: ...


assert_type(path("v1/", v1), URLPattern)
assert_type(path("v2/", v2), URLPattern)
assert_type(re_path("^v1/", v1), URLPattern)
assert_type(re_path("^v2/", v2), URLPattern)

# Test 'include'
patterns1: List[_AnyURL] = []
assert_type(re_path(_("^foo/"), include(patterns1)), URLResolver)
assert_type(re_path("^foo/", include(patterns1, namespace="foo")), URLResolver)
assert_type(re_path("^foo/", include((patterns1, "foo"), namespace="foo")), URLResolver)
assert_type(re_path("^foo/", include(patterns1, "foo")), URLResolver)
assert_type(path("flat/", include(flatpages_urls)), URLResolver)
assert_type(path("flat/", include((flatpages_urls, "static"))), URLResolver)
assert_type(path("i18n/", include(i18n_urlpatterns)), URLResolver)
assert_type(path("i18n/", include((i18n_urlpatterns, "i18n"))), URLResolver)
assert_type(path("admindocs/", include("django.contrib.admindocs.urls")), URLResolver)
assert_type(path("admindocs/", include(("django.contrib.admindocs.urls", "i18n"))), URLResolver)
assert_type(path("", include(staticfiles_urlpatterns(prefix="static/"))), URLResolver)
