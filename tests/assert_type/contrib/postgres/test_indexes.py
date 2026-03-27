from django.contrib.postgres.indexes import BrinIndex, BTreeIndex, GinIndex, GistIndex, HashIndex, OpClass, SpGistIndex
from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower

# BrinIndex
BrinIndex(fields=["foo"])
BrinIndex(models.F("bar"), name="test")
BrinIndex("foo", models.F("bar"), Lower("baz"), name="test")
BrinIndex("foo", name="test", opclasses=["bar"])
BrinIndex("foo", name="test", condition=models.Q(foo=1))
BrinIndex("foo", name="test", include=["bar"])

# BTreeIndex
BTreeIndex(fields=["foo"])
BTreeIndex(models.F("bar"), name="test")
BTreeIndex("foo", models.F("bar"), Lower("baz"), name="test")
BTreeIndex("foo", name="test", opclasses=["bar"])
BTreeIndex("foo", name="test", condition=models.Q(foo=1))
BTreeIndex("foo", name="test", include=["bar"])

# GinIndex
GinIndex(fields=["foo"])
GinIndex(models.F("bar"), name="test")
GinIndex("foo", models.F("bar"), Lower("baz"), name="test")
GinIndex("foo", name="test", opclasses=["bar"])
GinIndex("foo", name="test", condition=models.Q(foo=1))
GinIndex("foo", name="test", include=["bar"])

# GistIndex
GistIndex(fields=["foo"])
GistIndex(models.F("bar"), name="test")
GistIndex("foo", models.F("bar"), Lower("baz"), name="test")
GistIndex("foo", name="test", opclasses=["bar"])
GistIndex("foo", name="test", condition=models.Q(foo=1))
GistIndex("foo", name="test", include=["bar"])

# HashIndex
HashIndex(fields=["foo"])
HashIndex(models.F("bar"), name="test")
HashIndex("foo", models.F("bar"), Lower("baz"), name="test")
HashIndex("foo", name="test", opclasses=["bar"])
HashIndex("foo", name="test", condition=models.Q(foo=1))
HashIndex("foo", name="test", include=["bar"])

# SpGistIndex
SpGistIndex(fields=["foo"])
SpGistIndex(models.F("bar"), name="test")
SpGistIndex("foo", models.F("bar"), Lower("baz"), name="test")
SpGistIndex("foo", name="test", opclasses=["bar"])
SpGistIndex("foo", name="test", condition=models.Q(foo=1))
SpGistIndex("foo", name="test", include=["bar"])

# OpClass
Index(
    OpClass(Lower("username"), name="varchar_pattern_ops"),
    name="lower_username_idx",
)
