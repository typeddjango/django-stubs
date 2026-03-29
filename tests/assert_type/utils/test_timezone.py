from datetime import date, datetime, time
from typing import Literal

from django.utils.timezone import is_aware, is_naive
from typing_extensions import assert_type

# is_naive
is_naive(date(2020, 1, 1))  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
assert_type(is_naive(datetime(2020, 1, 1)), bool)
assert_type(is_naive(time()), Literal[True])

# is_aware
is_aware(date(2020, 1, 1))  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
assert_type(is_aware(datetime(2020, 1, 1)), bool)
assert_type(is_aware(time()), Literal[False])
