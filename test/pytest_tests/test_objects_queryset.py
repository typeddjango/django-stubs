from test.pytest_plugin import reveal_type, output
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestObjectsQueryset(BaseDjangoPluginTestCase):
    def test_every_model_has_objects_queryset_available(self):
        from django.db import models

        class User(models.Model):
            pass

        reveal_type(User.objects)  # E: Revealed type is 'django.db.models.query.QuerySet[main.User]'

    @output("""
main:10: error: Revealed type is 'Any'
main:10: error: "Type[ModelMixin]" has no attribute "objects"
    """)
    def test_objects_get_returns_model_instance(self):
        from django.db import models

        class ModelMixin(models.Model):
            class Meta:
                abstract = True

        class User(ModelMixin):
            pass

        reveal_type(User.objects.get())  # E: Revealed type is 'main.User*'
