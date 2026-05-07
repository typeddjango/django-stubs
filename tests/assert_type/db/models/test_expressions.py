from __future__ import annotations

import datetime
from decimal import Decimal

from django.db.models import F
from django.db.models.expressions import CombinedExpression
from typing_extensions import assert_type

now = datetime.datetime.now()
delta = datetime.timedelta(seconds=10)

assert_type(F("x") + now, CombinedExpression)
assert_type(now + F("x"), CombinedExpression)
assert_type(F("x") + delta, CombinedExpression)
assert_type(delta + F("x"), CombinedExpression)
assert_type(F("x") + 1, CombinedExpression)
assert_type(1 + F("x"), CombinedExpression)
assert_type(F("x") + 1.5, CombinedExpression)
assert_type(F("x") + Decimal(1), CombinedExpression)
assert_type(F("x") + F("y"), CombinedExpression)
assert_type(F("x") + "_suffix", CombinedExpression)
assert_type("prefix_" + F("x"), CombinedExpression)
assert_type(F("x") + None, CombinedExpression)
assert_type(None + F("x"), CombinedExpression)

assert_type(F("x") - now, CombinedExpression)
assert_type(now - F("x"), CombinedExpression)
assert_type(F("x") - delta, CombinedExpression)
assert_type(delta - F("x"), CombinedExpression)
assert_type(F("x") - 1, CombinedExpression)
assert_type(1 - F("x"), CombinedExpression)
assert_type(F("x") - 1.5, CombinedExpression)
assert_type(F("x") - Decimal(1), CombinedExpression)
assert_type(F("x") - F("y"), CombinedExpression)
assert_type(F("x") - None, CombinedExpression)
assert_type(None - F("x"), CombinedExpression)
