from re import Pattern
from typing import assert_type

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator

assert_type(RegexValidator.regex, str | Pattern[str])
assert_type(RegexValidator().regex, Pattern[str])

assert_type(UnicodeUsernameValidator.regex, str | Pattern[str])
assert_type(UnicodeUsernameValidator().regex, Pattern[str])
