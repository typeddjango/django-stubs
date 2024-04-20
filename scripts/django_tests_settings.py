# It is used in `mypy.ini` only.
# The following installed apps are required for stubtest to run correctly.
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
]

STATIC_URL = "static/"
