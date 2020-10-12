from django.db.backends.base.validation import BaseDatabaseValidation as BaseDatabaseValidation
from typing import Any

class DatabaseValidation(BaseDatabaseValidation):
    def check_field_type(self, field: Any, field_type: Any): ...
