from __future__ import annotations

from django.db import models


def unknown_constructor_kwarg_is_rejected() -> None:
    models.IntegerField(nul=True)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]


def file_field_rejects_primary_key() -> None:
    # Django's system check rejects it (fields.E201)
    models.FileField(primary_key=True)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]  # pyrefly: ignore[unexpected-keyword]  # ty: ignore[unknown-argument]
