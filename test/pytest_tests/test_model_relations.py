from test.pytest_plugin import MypyTypecheckTestCase, reveal_type


class BaseDjangoPluginTestCase(MypyTypecheckTestCase):
    def ini_file(self):
        return """
[mypy]
plugins = mypy_django_plugin.main
        """


class MyTestCase(BaseDjangoPluginTestCase):
    def check_foreign_key_field(self):
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

    def check_every_foreign_key_creates_field_name_with_appended_id(self):
        from django.db import models

        class Publisher(models.Model):
            pass

        class Book(models.Model):
            publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE,
                                          related_name='books')

        book = Book()
        reveal_type(book.publisher_id)  # E: Revealed type is 'builtins.int'

    def check_foreign_key_different_order_of_params(self):
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
