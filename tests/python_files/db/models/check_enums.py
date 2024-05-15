from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class MyIntegerChoices(IntegerChoices):
    A = 1
    B = 2, "B"
    C = 3, "B", "..."  # type: ignore
    D = 4, _("D")
    E = 5, 1  # type: ignore
    F = "1"


class MyTextChoices(TextChoices):
    A = "a"
    B = "b", "B"
    C = "c", _("C")
    D = 1  # type: ignore
    E = "e", 1  # type: ignore
