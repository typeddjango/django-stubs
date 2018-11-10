from typing import Optional

from django.core.handlers.wsgi import WSGIHandler


def get_wsgi_application() -> WSGIHandler: ...
