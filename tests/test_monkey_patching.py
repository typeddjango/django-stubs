import django
from django.conf import global_settings, settings
from django.contrib import admin
from django.db import models

import django_stubs_ext

django_stubs_ext.monkeypatch()

# important: if you change the filename, you need to change the INSTALLED_APPS
settings.configure(global_settings, INSTALLED_APPS=["test_monkey_patching"])

django.setup()


def test_model_admin_subscript():
    class Foo(models.Model):
        pass

    class FooAdmin(admin.ModelAdmin[Foo]):
        pass
