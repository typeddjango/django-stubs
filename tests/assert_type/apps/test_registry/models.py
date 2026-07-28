from __future__ import annotations

from typing import Any

from django.apps import apps
from django.apps.registry import apps as registry_apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.migrations.state import ProjectState
from typing_extensions import assert_type


class First(models.Model):
    pass


class Second(models.Model):
    pass


def get_model_resolves_literal_references() -> None:
    # Mypy plugin is needed to narrow `type[Any]` to type[MyModel]
    # TODO: other type checker should also understand that
    assert_type(apps.get_model("test_registry.First"), type[First])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(apps.get_model("test_registry.first"), type[First])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(apps.get_model("test_registry", "First"), type[First])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(apps.get_model(app_label="test_registry", model_name="first"), type[First])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(apps.get_model(model_name="Second", app_label="test_registry"), type[Second])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(registry_apps.get_model("contenttypes.ContentType"), type[ContentType])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]


def get_model_of_unknown_or_dynamic_reference_is_permissive() -> None:
    # Unknown models can't be resolved: the mypy plugin reports an error
    # TODO: other type checker should also raise issues here
    assert_type(apps.get_model("test_registry.Missing"), type[Any])  # type: ignore[misc]
    assert_type(apps.get_model("TEST_REGISTRY.First"), type[Any])  # type: ignore[misc]
    app_label = "test_registry"
    model = apps.get_model(app_label, "First")
    assert_type(model, type[Any])
    model.objects.whatever()


def get_model_of_historical_state_is_not_narrowed() -> None:
    # `StateApps` returns historical models rebuilt from migration state, so skip narrowing.
    state_apps = ProjectState().apps
    assert_type(state_apps.get_model("test_registry.First"), type[Any])
