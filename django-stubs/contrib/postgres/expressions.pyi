from django.contrib.postgres.fields import ArrayField
from django.db.models import Subquery
from django.utils.functional import cached_property

class ArraySubquery(Subquery):
    template: str

    @cached_property
    def output_field(self) -> ArrayField: ...
