from __future__ import annotations

from mypy.errorcodes import ErrorCode

MANAGER_MISSING = ErrorCode("django-manager-missing", "Couldn't resolve manager for model", "Django")
