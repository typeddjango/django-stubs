from test.pytest_plugin import reveal_type, output
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestObjectsQueryset(BaseDjangoPluginTestCase):
    def test_every_model_has_objects_queryset_available(self):
        from django.db import models

        class User(models.Model):
            pass

        reveal_type(User.objects)  # E: Revealed type is 'django.db.models.query.QuerySet[main.User]'
        reveal_type(User.objects.get())  # E: Revealed type is 'main.User*'
