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


GDAL_LIBRARY_PATH = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
