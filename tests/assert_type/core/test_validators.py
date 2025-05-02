import re
from re import Pattern

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from typing_extensions import assert_type

assert_type(RegexValidator.regex, str | Pattern[str])
assert_type(RegexValidator().regex, Pattern[str])
RegexValidator().regex = re.compile("")

assert_type(UnicodeUsernameValidator.regex, str | Pattern[str])
assert_type(UnicodeUsernameValidator().regex, Pattern[str])
UnicodeUsernameValidator().regex = re.compile("")

# expect "Pattern[str]"
RegexValidator().regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]
UnicodeUsernameValidator().regex = ""  # type: ignore[assignment] # pyright: ignore[reportAttributeAccessIssue]

# expect "_ClassOrInstanceAttribute[Union[str, Pattern[str]], Pattern[str]]"
RegexValidator.regex = "anything fails here"  # type: ignore[assignment]
UnicodeUsernameValidator.regex = "anything fails here"  # type: ignore[assignment]
