from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

reversed_url = reverse("url")
lazy_url = reverse_lazy("namespace:url")

HttpResponseRedirect(reversed_url)
HttpResponseRedirect(lazy_url)
HttpResponseRedirect(settings.LOGIN_URL)
HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
