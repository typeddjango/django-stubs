from __future__ import annotations

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.finders import AppDirectoriesFinder, BaseFinder, DefaultStorageFinder, FileSystemFinder
from typing_extensions import assert_type

# find (single)
assert_type(finders.find("filepath"), str | None)

for finder in finders.get_finders():
    assert_type(finder, BaseFinder)
    assert_type(finder.find("filepath"), str | None)

assert_type(FileSystemFinder().find("filepath"), str | None)
assert_type(AppDirectoriesFinder().find("filepath"), str | None)
assert_type(DefaultStorageFinder().find("filepath"), str | None)

# find (all)
assert_type(finders.find("filepath", find_all=True), list[str])

for finder in finders.get_finders():
    assert_type(finder.find("filepath", find_all=True), list[str])  # ty: ignore[type-assertion-failure]

assert_type(FileSystemFinder().find("filepath", find_all=True), list[str])  # ty: ignore[type-assertion-failure]
assert_type(AppDirectoriesFinder().find("filepath", find_all=True), list[str])  # ty: ignore[type-assertion-failure]
assert_type(DefaultStorageFinder().find("filepath", find_all=True), list[str])  # ty: ignore[type-assertion-failure]

# find (deprecated `all` kwarg, removed in Django 6.1)
assert_type(finders.find("filepath", all=False), str | None)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]
assert_type(finders.find("filepath", all=True), list[str])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]
assert_type(FileSystemFinder().find("filepath", all=True), list[str])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]
assert_type(AppDirectoriesFinder().find("filepath", all=True), list[str])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]
assert_type(DefaultStorageFinder().find("filepath", all=True), list[str])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]

for finder in finders.get_finders():
    assert_type(finder.find("filepath", all=False), str | None)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]
    assert_type(finder.find("filepath", all=True), list[str])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]

# FileSystemFinder-specific
assert_type(FileSystemFinder().find_location(".", "filepath"), str | None)

# AppDirectoriesFinder-specific
assert_type(AppDirectoriesFinder().find_in_app("app", "filepath"), str | None)
