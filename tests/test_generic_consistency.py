import ast
import glob
import importlib
import os
from typing import Any, final
from unittest import mock

import django

from django_stubs_ext.patch import MPGeneric

# The root directory of the django-stubs package
STUBS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "django-stubs"))


@final
class GenericInheritanceVisitor(ast.NodeVisitor):
    """AST visitor to find classes inheriting from `typing.Generic` in stubs."""

    def __init__(self) -> None:
        self.generic_classes: set[str] = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for base in node.bases:
            if (
                isinstance(base, ast.Subscript)
                and isinstance(base.value, ast.Name)
                and base.value.id == "Generic"
                and not any(dec.id == "type_check_only" for dec in node.decorator_list if isinstance(dec, ast.Name))
            ):
                self.generic_classes.add(node.name)
                break
        self.generic_visit(node)


def test_find_classes_inheriting_from_generic() -> None:
    """
    This test ensures that the `ext/django_stubs_ext/patch.py` stays up-to-date with the stubs.
    It works as follows:
        1. Parse the ast of each .pyi file, and collects classes inheriting from Generic.
        2. For each Generic in the stubs, import the associated module and capture every class in the MRO
        3. Ensure that at least one class in the mro is patched in `ext/django_stubs_ext/patch.py`.
    """
    with mock.patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": "scripts.django_tests_settings"}):
        # We need this to be able to do django import
        django.setup()

    # A dict of class_name -> [subclasses names] for each Generic in the stubs.
    all_generic_classes: dict[str, list[str]] = {}

    print(f"Searching for classes inheriting from Generic in: {STUBS_ROOT}")
    pyi_files = glob.glob("**/*.pyi", root_dir=STUBS_ROOT, recursive=True)
    for file_path in pyi_files:
        with open(os.path.join(STUBS_ROOT, file_path)) as f:
            source = f.read()

        tree = ast.parse(source)
        generic_visitor = GenericInheritanceVisitor()
        generic_visitor.visit(tree)

        # For each Generic in the stubs, import the associated module and capture every class in the MRO
        if generic_visitor.generic_classes:
            module_name = _get_module_from_pyi(file_path)
            django_module = importlib.import_module(module_name)
            all_generic_classes.update(
                {
                    cls: [subcls.__name__ for subcls in getattr(django_module, cls).mro()[1:-1]]
                    for cls in generic_visitor.generic_classes
                }
            )

    print(f"Processed {len(pyi_files)} .pyi files.")
    print(f"Found {len(all_generic_classes)} unique classes inheriting from Generic in stubs")

    patched_classes = {mp_generic.cls.__name__ for mp_generic in _get_need_generic()}

    # Pretty-print missing patch in `ext/django_stubs_ext/patch.py`
    errors = []
    for cls_name, subcls_names in all_generic_classes.items():
        if not any(name in patched_classes for name in [*subcls_names, cls_name]):
            bases = f"({', '.join(subcls_names)})" if subcls_names else ""
            errors.append(f"{cls_name}{bases} is not patched in `ext/django_stubs_ext/patch.py`")

    assert not errors, "\n".join(errors)


def _get_module_from_pyi(pyi_path: str) -> str:
    py_module = "django." + pyi_path.replace(".pyi", "").replace("/", ".")
    return py_module.removesuffix(".__init__")


def _get_need_generic() -> list[MPGeneric[Any]]:
    """
    Symbols in `django.contrib.auth.forms` are very hard to patch automatically
    because we end up importing the User model and it crashes if `django.setup()` was not called beforehand.
    It can also very easily introduce circular imports so we require the user to monkeypatch it manually.
    See README.md for more details
    """

    import django_stubs_ext

    if django.VERSION >= (5, 1):
        from django.contrib.auth.forms import SetPasswordMixin, SetUnusablePasswordMixin

        return [MPGeneric(SetPasswordMixin), MPGeneric(SetUnusablePasswordMixin), *django_stubs_ext.patch._need_generic]
    else:
        from django.contrib.auth.forms import AdminPasswordChangeForm, SetPasswordForm

        return [MPGeneric(SetPasswordForm), MPGeneric(AdminPasswordChangeForm), *django_stubs_ext.patch._need_generic]
