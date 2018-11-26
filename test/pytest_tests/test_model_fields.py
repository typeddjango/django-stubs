from test.pytest_plugin import reveal_type
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestBasicModelFields(BaseDjangoPluginTestCase):
    def test_model_field_classes_present_as_primitives(self):
        from django.db import models

        class User(models.Model):
            id = models.AutoField(primary_key=True)
            small_int = models.SmallIntegerField()
            name = models.CharField(max_length=255)
            slug = models.SlugField(max_length=255)
            text = models.TextField()

        user = User()
        reveal_type(user.id)  # E: Revealed type is 'builtins.int'
        reveal_type(user.small_int)  # E: Revealed type is 'builtins.int'
        reveal_type(user.name)  # E: Revealed type is 'builtins.str'
        reveal_type(user.slug)  # E: Revealed type is 'builtins.str'
        reveal_type(user.text)  # E: Revealed type is 'builtins.str'
