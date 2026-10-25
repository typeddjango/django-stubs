from __future__ import annotations

from typing import assert_type

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site
from django.contrib.auth.models import User

assert_type(site.get_model_admin(User), ModelAdmin[User])
