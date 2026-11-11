from __future__ import annotations

import django.contrib.auth.urls as auth_urls
from django.urls import get_resolver, is_valid_path, resolve, reverse, reverse_lazy

# `urlconf` takes a module as well as a dotted path
resolve("/login/", urlconf=auth_urls)
reverse("login", urlconf=auth_urls)
reverse_lazy("login", urlconf=auth_urls)
is_valid_path("/login/", urlconf=auth_urls)
get_resolver(auth_urls)
