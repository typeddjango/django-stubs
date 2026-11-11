from __future__ import annotations

from django.core.validators import URLValidator

# Runtime only checks `scheme in self.schemes`
URLValidator(schemes=["http", "https"])
URLValidator(schemes={"http", "https"})
URLValidator(schemes=frozenset({"git"}))
