from test.pytest_plugin import reveal_type
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestForeignKey(BaseDjangoPluginTestCase):
    def test_foreign_key_field(self):
        from django.db import models

        class Publisher(models.Model):
            pass

        class Book(models.Model):
            publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE,
                                          related_name='books')

        book = Book()
        reveal_type(book.publisher)  # E: Revealed type is 'main.Publisher*'

        publisher = Publisher()
        reveal_type(publisher.books)  # E: Revealed type is 'django.db.models.query.QuerySet[main.Book]'

    def test_every_foreign_key_creates_field_name_with_appended_id(self):
        from django.db import models

        class Publisher(models.Model):
            pass

        class Book(models.Model):
            publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE,
                                          related_name='books')

        book = Book()
        reveal_type(book.publisher_id)  # E: Revealed type is 'builtins.int'

    def test_foreign_key_different_order_of_params(self):
        from django.db import models

        class Publisher(models.Model):
            pass

        class Book(models.Model):
            publisher = models.ForeignKey(on_delete=models.CASCADE, to=Publisher,
                                          related_name='books')

        book = Book()
        reveal_type(book.publisher)  # E: Revealed type is 'main.Publisher*'

        publisher = Publisher()
        reveal_type(publisher.books)  # E: Revealed type is 'django.db.models.query.QuerySet[main.Book]'


class TestOneToOneField(BaseDjangoPluginTestCase):
    def test_onetoone_field(self):
        from django.db import models

        class User(models.Model):
            pass

        class Profile(models.Model):
            user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')

        profile = Profile()
        reveal_type(profile.user)  # E: Revealed type is 'main.User*'

        user = User()
        reveal_type(user.profile)  # E: Revealed type is 'main.Profile'

    def test_onetoone_field_with_underscore_id(self):
        from django.db import models

        class User(models.Model):
            pass

        class Profile(models.Model):
            user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')

        profile = Profile()
        reveal_type(profile.user_id)  # E: Revealed type is 'builtins.int'

    def test_parameter_to_keyword_may_be_absent(self):
        from django.db import models

        class User(models.Model):
            pass

        class Profile(models.Model):
            user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

        reveal_type(User().profile)  # E: Revealed type is 'main.Profile'
