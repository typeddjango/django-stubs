from __future__ import annotations

import ast
import glob
import importlib
import os
from pathlib import Path
from typing import Any, final
from unittest import mock

import django
from typing_extensions import override

# The root directory of the django-stubs package
STUBS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "django-stubs"))


@final
class GenericInheritanceVisitor(ast.NodeVisitor):
    """AST visitor collecting type variables and classes with parameterized bases in the stubs."""

    def __init__(self) -> None:
        self.module = ""
        # Type variables are collected from `X = TypeVar(...)` assignments. `AnyStr` is declared
        # in `typing` itself, not in the stubs, so it must be seeded manually.
        self.type_vars: set[str] = {"AnyStr"}
        # (module, class_name) -> {names parameterizing its bases}.
        # A class is generic if one of those names is a type variable
        self.candidate_classes: dict[tuple[str, str], set[str]] = {}

    @override
    def visit_Assign(self, node: ast.Assign) -> None:
        func = node.value.func if isinstance(node.value, ast.Call) else None
        if isinstance(func, ast.Name) and func.id in {"TypeVar", "ParamSpec", "TypeVarTuple"}:
            self.type_vars.update(target.id for target in node.targets if isinstance(target, ast.Name))

    @override
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for base in node.bases:
            if isinstance(base, ast.Subscript):
                self.candidate_classes.setdefault((self.module, node.name), set()).update(
                    name.id for name in ast.walk(base.slice) if isinstance(name, ast.Name)
                )
        self.generic_visit(node)


def test_generic_classes_are_subscriptable_at_runtime() -> None:
    """
    Ensure `ext/django_stubs_ext/patch.py` stays up-to-date with the stubs.
    Every class that is generic in the stubs must be subscriptable at runtime once `monkeypatch()` is called.
    """
    with mock.patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": "scripts.django_tests_settings"}):
        django.setup()

    _monkeypatch()

    visitor = GenericInheritanceVisitor()
    for file_path in glob.glob("**/*.pyi", root_dir=STUBS_ROOT, recursive=True):
        visitor.module = "django." + file_path.replace(".pyi", "").replace("/", ".").removesuffix(".__init__")
        visitor.visit(ast.parse(Path(STUBS_ROOT, file_path).read_text()))

    errors = []
    for (module_name, cls_name), base_args in visitor.candidate_classes.items():
        if not base_args & visitor.type_vars:
            # Bases are only parameterized by concrete types (e.g. `Iterable[bytes]`)
            continue

        try:
            django_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

        if (cls := getattr(django_module, cls_name, None)) is None:
            # `type_check_only`, or doesn't exist in the Django version being tested
            continue

        try:
            cls[Any]
        except TypeError:
            errors.append(f"{module_name}.{cls_name} is not patched in `ext/django_stubs_ext/patch.py`")

    assert not errors, "\n".join(errors)


def _monkeypatch() -> None:
    """
    Symbols in `django.contrib.auth.forms` are very hard to patch automatically
    because we end up importing the User model and it crashes if `django.setup()` was not called beforehand.
    It can also very easily introduce circular imports so we require the user to monkeypatch it manually.
    See README.md for more details
    """

    import django_stubs_ext

    if django.VERSION >= (5, 1):
        from django.contrib.auth.forms import SetPasswordMixin, SetUnusablePasswordMixin

        extra_classes: list[type] = [SetPasswordMixin, SetUnusablePasswordMixin]
    else:
        from django.contrib.auth.forms import AdminPasswordChangeForm, SetPasswordForm

        extra_classes = [SetPasswordForm, AdminPasswordChangeForm]

    django_stubs_ext.monkeypatch(extra_classes=extra_classes)
