import django
from django.conf import global_settings, settings
from django.contrib import admin
from django.db import models

import django_stubs

django_stubs.monkeypatch()

settings.configure(global_settings, INSTALLED_APPS=["thing"])

django.setup()


def test_model_admin_subscript():
    class Foo(models.Model):
        pass

    class FooAdmin(admin.ModelAdmin[Foo]):
        pass
