from django.http.request import HttpRequest
from django.utils.safestring import SafeText


def csrf_input(request: HttpRequest) -> SafeText: ...