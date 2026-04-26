# It is used in `mypy.ini` only.
# The following installed apps are required for stubtest to run correctly.
from __future__ import annotations

import pathlib

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_ASSERT_TYPE_APPS_ROOT = _REPO_ROOT / "tests" / "assert_type" / "_apps"


def _discover_assert_type_apps() -> list[str]:
    """Discover Django apps under ``tests/assert_type/_apps/``.

    Each directory containing a ``models.py`` is registered as an app, with
    the directory name as the implicit ``app_label``. This lets each migrated
    YAML case keep its own isolated set of models without collisions.
    """
    if not _ASSERT_TYPE_APPS_ROOT.is_dir():
        return []
    return sorted(
        ".".join(models_py.parent.relative_to(_REPO_ROOT).parts)
        for models_py in _ASSERT_TYPE_APPS_ROOT.rglob("models.py")
    )


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    *_discover_assert_type_apps(),
]

STATIC_URL = "static/"
