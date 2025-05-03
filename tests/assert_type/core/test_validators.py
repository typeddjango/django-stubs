import re
from re import Pattern

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from typing_extensions import assert_type

assert_type(RegexValidator().regex, Pattern[str])
RegexValidator().regex = re.compile("")

assert_type(UnicodeUsernameValidator().regex, Pattern[str])
UnicodeUsernameValidator().regex = re.compile("")

# expect "Pattern[str]"
RegexValidator().regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]
UnicodeUsernameValidator().regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]


class RegexSubtype(RegexValidator):
    regex = re.compile("abc")


# We would like to improve on these, it should allow "str | Pattern[str]":
assert_type(RegexValidator.regex, Pattern[str])
assert_type(UnicodeUsernameValidator.regex, Pattern[str])

RegexValidator.regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]
UnicodeUsernameValidator.regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]


class StrSubtype(RegexValidator):
    regex = "abc"  # type: ignore[assignment] # pyright: ignore[reportAssignmentType]
