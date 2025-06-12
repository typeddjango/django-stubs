import enum
from typing import Any, Literal, TypeVar

from django.db.models import Choices, IntegerChoices, Model, TextChoices
from django.utils.functional import _StrOrPromise
from django.utils.translation import gettext_lazy as _
from typing_extensions import assert_type

# Choices in a separate model to test that the plugin resolves types correctly.
from tests.assert_type.db.models import _enums as imported

T_Choices = TypeVar("T_Choices", bound=IntegerChoices)


def get_choices_using_property(choices: type[T_Choices]) -> list[tuple[int, str]]:
    return choices.choices  # pyright: ignore[reportReturnType]


def get_labels_using_property(choices: type[T_Choices]) -> list[str]:
    return choices.labels  # pyright: ignore[reportReturnType]


def get_values_using_property(choices: type[T_Choices]) -> list[int]:
    return choices.values


def get_labels_using_comprehension(choices: type[T_Choices]) -> list[str]:
    return [choice.label for choice in choices]  # pyright: ignore[reportReturnType]


def get_values_using_comprehension(choices: type[T_Choices]) -> list[int]:
    return [choice.value for choice in choices]


class Suit(IntegerChoices):
    DIAMOND = 1, _("Diamond")
    SPADE = 2, _("Spade")
    HEART = 3, _("Heart")
    CLUB = 4, _("Club")


class YearInSchool(TextChoices):
    FRESHMAN = "FR", _("Freshman")
    SOPHOMORE = "SO", _("Sophomore")
    JUNIOR = "JR", _("Junior")
    SENIOR = "SR", _("Senior")
    GRADUATE = "GR", _("Graduate")


class Vehicle(IntegerChoices):
    CAR = 1, "Carriage"
    TRUCK = 2
    JET_SKI = 3

    __empty__ = _("(Unknown)")


class Gender(TextChoices):
    MALE = "M"
    FEMALE = "F"
    NOT_SPECIFIED = "X"

    __empty__ = "(Undeclared)"


class Medal(TextChoices):
    GOLD = enum.auto()
    SILVER = enum.auto()
    BRONZE = enum.auto()


class Separator(bytes, Choices):
    FS = b"\x1c", "File Separator"
    GS = b"\x1d", "Group Separator"
    RS = b"\x1e", "Record Separator"
    US = b"\x1f", "Unit Separator"


class Constants(float, Choices):
    PI = 3.141592653589793, "π"
    TAU = 6.283185307179586, "τ"

    __empty__ = "NULL"


class BaseEmptyChoices(Choices):
    __empty__ = "Python's None"


class VoidChoices(BaseEmptyChoices):
    ABYSS = enum.auto()
    CHASM = enum.auto()


# Choice type that has been aliased to test that the plugin resolves types correctly.
CompassPoint = imported.Direction


# Choice type that has been aliased by type to test that the plugin resolves types correctly.
Award: type[TextChoices] = Medal


# Checks unions of enum literals to test that the plugin resolves types correctly.
def get_suit_with_color(suit: Suit) -> str:
    if suit == Suit.DIAMOND or suit == Suit.HEART:
        return f"{suit.label} is red."
    else:
        return f"{suit.label} is black."


# Checks a single enum literal to test that the plugin resolves types correctly.
def is_suit_a_diamond(suit: Suit) -> str:
    if suit == Suit.DIAMOND:
        return f"{suit.label}: Yes!"
    else:
        return f"{suit.label}: No!"


# Choice type that overrides a property and uses `super()` to test the plugin resolve types correctly.
class ShoutyTextChoices(TextChoices):
    @property
    def label(self) -> str:
        return super().label.upper()


class DeckModel(Model):
    # Alias with the same name.
    Suit = Suit

    # Alias with a different name.
    House = Suit

    class Joker(TextChoices):
        BLACK = "B"
        RED = "R"


# Assertions for an integer choices type that uses a lazy translatable string for all labels.
assert_type(Suit.names, list[str])
assert_type(Suit.labels, list[_StrOrPromise])
assert_type(Suit.values, list[int])
assert_type(Suit.choices, list[tuple[int, _StrOrPromise]])
assert_type(Suit.CLUB, Literal[Suit.CLUB])
assert_type(Suit.CLUB.name, Literal["CLUB"])
assert_type(Suit.CLUB.label, _StrOrPromise)
assert_type(Suit.CLUB.value, int)
assert_type(Suit.CLUB.do_not_call_in_templates, Literal[True])

# Assertions for a text choices type that uses a lazy translatable string for all labels.
assert_type(YearInSchool.names, list[str])
assert_type(YearInSchool.labels, list[_StrOrPromise])
assert_type(YearInSchool.values, list[str])
assert_type(YearInSchool.choices, list[tuple[str, _StrOrPromise]])
assert_type(YearInSchool.SENIOR, Literal[YearInSchool.SENIOR])
assert_type(YearInSchool.SENIOR.name, Literal["SENIOR"])
assert_type(YearInSchool.SENIOR.label, _StrOrPromise)
assert_type(YearInSchool.SENIOR.value, str)
assert_type(YearInSchool.SENIOR.do_not_call_in_templates, Literal[True])

# Assertions for an integer choices type that defines `__empty__`, generates most labels, etc.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
assert_type(Vehicle.names, list[str])
assert_type(Vehicle.labels, list[_StrOrPromise])
assert_type(Vehicle.values, list[int | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Vehicle.choices, list[tuple[int | None, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Vehicle.CAR, Literal[Vehicle.CAR])
assert_type(Vehicle.CAR.name, Literal["CAR"])
assert_type(Vehicle.CAR.label, _StrOrPromise)
assert_type(Vehicle.CAR.value, int)
assert_type(Vehicle.CAR.do_not_call_in_templates, Literal[True])
assert_type(Vehicle.__empty__, _StrOrPromise)

# Assertions for an text choices type that defines `__empty__` and uses plain strings for all labels.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Gender.names, list[str])
assert_type(Gender.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.values, list[str | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.choices, list[tuple[str | None, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.MALE, Literal[Gender.MALE])
assert_type(Gender.MALE.name, Literal["MALE"])
assert_type(Gender.MALE.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.MALE.value, str)
assert_type(Gender.MALE.do_not_call_in_templates, Literal[True])
assert_type(Gender.__empty__, str)  # pyright: ignore[reportAssertTypeFailure]

# Assertions for a text choices type that uses `enum.auto()`.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Medal.names, list[str])
assert_type(Medal.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Medal.values, list[str])
assert_type(Medal.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Medal.GOLD, Literal[Medal.GOLD])
assert_type(Medal.GOLD.name, Literal["GOLD"])
assert_type(Medal.GOLD.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Medal.GOLD.value, str)
assert_type(Medal.GOLD.do_not_call_in_templates, Literal[True])

# Assertions for a choices type that uses a custom base type.
# Note: Suppress errors from pyright as the mypy plugin handles propagating custom base types.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Separator.names, list[str])
assert_type(Separator.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.values, list[bytes])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.choices, list[tuple[bytes, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.FS, Literal[Separator.FS])
assert_type(Separator.FS.name, Literal["FS"])
assert_type(Separator.FS.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.FS.value, bytes)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.FS.do_not_call_in_templates, Literal[True])

# Assertions for a choices type uses a custom base type and defines `__empty__`.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
# Note: Suppress errors from pyright as the mypy plugin handles propagating custom base types.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Constants.names, list[str])
assert_type(Constants.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.values, list[float | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.choices, list[tuple[float | None, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.PI, Literal[Constants.PI])
assert_type(Constants.PI.name, Literal["PI"])
assert_type(Constants.PI.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.PI.value, float)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.PI.do_not_call_in_templates, Literal[True])
assert_type(Constants.__empty__, str)  # pyright: ignore[reportAssertTypeFailure]

# Assertions for a choices type where `__empty__` is defined on a base class.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(VoidChoices.names, list[str])
assert_type(VoidChoices.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.values, list[Any | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.choices, list[tuple[Any | None, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.ABYSS, Literal[VoidChoices.ABYSS])
assert_type(VoidChoices.ABYSS.name, Literal["ABYSS"])
assert_type(VoidChoices.ABYSS.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.ABYSS.value, Any)
assert_type(VoidChoices.ABYSS.do_not_call_in_templates, Literal[True])
assert_type(VoidChoices.__empty__, str)  # pyright: ignore[reportAssertTypeFailure]

# Assertions for a choices type imported from another module to test the plugin resolves correctly.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(imported.Direction.names, list[str])
assert_type(imported.Direction.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(imported.Direction.values, list[str])
assert_type(imported.Direction.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(imported.Direction.NORTH, Literal[imported.Direction.NORTH])
assert_type(imported.Direction.NORTH.name, Literal["NORTH"])
assert_type(imported.Direction.NORTH.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(imported.Direction.NORTH.value, str)
assert_type(imported.Direction.NORTH.do_not_call_in_templates, Literal[True])

# Assertions for a choices type aliased from another to test the plugin resolves correctly.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(CompassPoint.names, list[str])
assert_type(CompassPoint.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(CompassPoint.values, list[str])
assert_type(CompassPoint.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(CompassPoint.NORTH, Literal[imported.Direction.NORTH])
assert_type(CompassPoint.NORTH.name, Literal["NORTH"])
assert_type(CompassPoint.NORTH.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(CompassPoint.NORTH.value, str)
assert_type(CompassPoint.NORTH.do_not_call_in_templates, Literal[True])

# Assertions for a choices type aliased by type to test the plugin resolves correctly.
# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Award.names, list[str])
assert_type(Award.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Award.values, list[str])
assert_type(Award.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]

# Assertions for mixing multiple choices types with consistent base types - only `IntegerChoices`.
x0 = (Suit, Vehicle)
assert_type([member.label for choices in x0 for member in choices], list[_StrOrPromise])
assert_type([member.value for choices in x0 for member in choices], list[int])

# Assertions for mixing multiple choices types with consistent base types - only `TextChoices`.
x1 = (Medal, Gender)
assert_type([member.label for choices in x1 for member in choices], list[_StrOrPromise])
assert_type([member.value for choices in x1 for member in choices], list[str])

# Assertions for mixing multiple choices types with different base types - `IntegerChoices` and `TextChoices`.
x2 = (Medal, Suit)
assert_type([member.label for choices in x2 for member in choices], list[_StrOrPromise])
assert_type([member.value for choices in x2 for member in choices], list[int | str])

# Assertions for mixing multiple choices types with consistent base types - custom types.
x3 = (Constants, Separator)
assert_type([member.label for choices in x3 for member in choices], list[_StrOrPromise])
assert_type([member.value for choices in x3 for member in choices], list[Any])


# Assertions for choices objects defined and aliased in a model.
assert_type(DeckModel.Suit.choices, list[tuple[int, _StrOrPromise]])
assert_type(DeckModel.House.choices, list[tuple[int, _StrOrPromise]])
assert_type(DeckModel.Joker.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]
