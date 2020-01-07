from typing import Mapping

from django.core.exceptions import ValidationError

def prefix_validation_error(error: ValidationError, prefix: str, code: str, params: Mapping) -> ValidationError: ...
