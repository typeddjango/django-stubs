from test.pytest_plugin import file, reveal_type, env
from test.pytest_tests.base import BaseDjangoPluginTestCase


class TestForeignKey(BaseDjangoPluginTestCase):
    @env(DJANGO_SETTINGS_MODULE='mysettings')
    def _test_to_parameter_could_be_specified_as_string(self):
        from apps.myapp.models import Publisher

        publisher = Publisher()
        reveal_type(publisher.books)  # E: Revealed type is 'django.db.models.query.QuerySet[apps.myapp2.models.Book]'

    # @env(DJANGO_SETTINGS_MODULE='mysettings')
    # def _test_creates_underscore_id_attr(self):
    #     from apps.myapp2.models import Book
    #
    #     book = Book()
    #     reveal_type(book.publisher)  # E: Revealed type is 'apps.myapp.models.Publisher'
    #     reveal_type(book.publisher_id)  # E: Revealed type is 'builtins.int'

    @file('mysettings.py')
    def mysettings(self):
        SECRET_KEY = '112233'
        ROOT_DIR = '<TMP>'
        APPS_DIR = '<TMP>/apps'

        INSTALLED_APPS = ('apps.myapp', 'apps.myapp2')

    @file('apps/myapp/models.py', make_parent_packages=True)
    def apps_myapp_models(self):
        from django.db import models

        class Publisher(models.Model):
            pass

    @file('apps/myapp2/models.py', make_parent_packages=True)
    def apps_myapp2_models(self):
        from django.db import models

        class Book(models.Model):
            publisher = models.ForeignKey(to='myapp.Publisher', on_delete=models.CASCADE,
                                          related_name='books')


class TestOneToOneField(BaseDjangoPluginTestCase):
    @env(DJANGO_SETTINGS_MODULE='mysettings')
    def test_to_parameter_could_be_specified_as_string(self):
        from apps.myapp.models import User

        user = User()
        reveal_type(user.profile)  # E: Revealed type is 'apps.myapp2.models.Profile'

    @file('mysettings.py')
    def mysettings(self):
        SECRET_KEY = '112233'
        ROOT_DIR = '<TMP>'
        APPS_DIR = '<TMP>/apps'

        INSTALLED_APPS = ('apps.myapp', 'apps.myapp2')

    @file('apps/myapp/models.py', make_parent_packages=True)
    def apps_myapp_models(self):
        from django.db import models

        class User(models.Model):
            pass

    @file('apps/myapp2/models.py', make_parent_packages=True)
    def apps_myapp2_models(self):
        from django.db import models

        class Profile(models.Model):
            user = models.OneToOneField(to='myapp.User', on_delete=models.CASCADE,
                                        related_name='profile')
