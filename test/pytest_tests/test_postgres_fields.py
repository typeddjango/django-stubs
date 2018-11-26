from test.pytest_plugin import reveal_type
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestArrayField(BaseDjangoPluginTestCase):
    def test_descriptor_access(self):
        from django.db import models
        from django.contrib.postgres.fields import ArrayField

        class User(models.Model):
            array = ArrayField(base_field=models.Field())

        user = User()
        reveal_type(user.array)  # E: Revealed type is 'builtins.list[Any]'

    def test_base_field_parsed_into_generic_attribute(self):
        from django.db import models
        from django.contrib.postgres.fields import ArrayField

        class User(models.Model):
            members = ArrayField(base_field=models.IntegerField())
            members_as_text = ArrayField(base_field=models.CharField(max_length=255))

        user = User()
        reveal_type(user.members)  # E: Revealed type is 'builtins.list[builtins.int*]'
        reveal_type(user.members_as_text)  # E: Revealed type is 'builtins.list[builtins.str*]'

