from __future__ import annotations

from typing import assert_type

from django.db import models

assert_type(models.CharField(max_length=100, db_collation="en-x-icu").db_collation, str | None)
assert_type(models.TextField(db_collation="en-x-icu").db_collation, str | None)
assert_type(models.SlugField(max_length=100, db_collation="en-x-icu").db_collation, str | None)
assert_type(models.URLField(db_collation="en-x-icu").db_collation, str | None)
assert_type(models.EmailField(db_collation="en-x-icu").db_collation, str | None)
