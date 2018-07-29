from django.contrib.auth.models import User


class AdminAuthenticationForm:
    def confirm_login_allowed(self, user: User) -> None: ...