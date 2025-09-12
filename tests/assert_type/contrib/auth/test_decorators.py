from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy

reversed_url = reverse("url")
lazy_url = reverse_lazy("namespace:url")


@user_passes_test(lambda user: user.is_active, login_url=reversed_url)
def my_view1(request: HttpRequest) -> HttpResponse: ...


@user_passes_test(lambda user: user.is_active, login_url=lazy_url)
def my_view2(request: HttpRequest) -> HttpResponse: ...
