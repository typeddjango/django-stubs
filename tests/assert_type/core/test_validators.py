import re
from re import Pattern
from typing import assert_type

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator

assert_type(RegexValidator.regex, str | Pattern[str])
assert_type(RegexValidator().regex, Pattern[str])
RegexValidator().regex = re.compile("")
RegexValidator().regex = ""  # type: ignore[assignment] # expect "Pattern[str]"
RegexValidator.regex = "anything fails here"  # type: ignore[assignment] # expect "_ClassOrInstanceAttribute[Union[str, Pattern[str]], Pattern[str]]"

assert_type(UnicodeUsernameValidator.regex, str | Pattern[str])
assert_type(UnicodeUsernameValidator().regex, Pattern[str])
UnicodeUsernameValidator().regex = re.compile("")
UnicodeUsernameValidator().regex = ""  # type: ignore[assignment] # expect "Pattern[str]"
UnicodeUsernameValidator.regex = "anything fails here"  # type: ignore[assignment] # expect "_ClassOrInstanceAttribute[Union[str, Pattern[str]], Pattern[str]]"
