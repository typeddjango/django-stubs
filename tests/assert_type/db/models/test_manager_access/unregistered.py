"""Not a `models.py`, so the app registry never loads these models and the plugin can't read their managers."""

from __future__ import annotations

from typing import assert_type

from django.db import models


class WithDefaultManager(models.Model):
    pass


class CustomManager(models.Manager["WithDeclaredManager"]):
    pass


class WithDeclaredManager(models.Model):
    objects = CustomManager()


def default_manager_falls_back_to_the_stub_declaration() -> None:
    assert_type(WithDefaultManager.objects, models.Manager[WithDefaultManager])


def default_manager_on_type_resolves_the_model(model: type[WithDefaultManager]) -> None:
    assert_type(model.objects.get(), WithDefaultManager)


def declared_manager_is_kept() -> None:
    assert_type(WithDeclaredManager.objects, CustomManager)
