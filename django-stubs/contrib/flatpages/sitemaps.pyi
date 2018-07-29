from django.db.models.query import QuerySet


class FlatPageSitemap:
    def items(self) -> QuerySet: ...