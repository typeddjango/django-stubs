from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.conf import settings

from django_stubs_ext.aliases import StrOrPromise

from typing import assert_type

reversed_url = reverse('url')
lazy_url = reverse_lazy('namespace:url')

HttpResponseRedirect(reversed_url)
HttpResponseRedirect(lazy_url)
HttpResponseRedirect(settings.LOGIN_URL)
HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

assert_type(settings.LOGIN_URL, StrOrPromise)
assert_type(settings.LOGIN_REDIRECT_URL, StrOrPromise)
assert_type(settings.LOGOUT_REDIRECT_URL, StrOrPromise | None)
