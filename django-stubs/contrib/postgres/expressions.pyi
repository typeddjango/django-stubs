from django.contrib.postgres.fields import ArrayField
from django.db.models import Subquery

class ArraySubquery(Subquery):
    template: str

    @property
    def output_field(self) -> ArrayField: ...
