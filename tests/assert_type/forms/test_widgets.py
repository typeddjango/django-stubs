from __future__ import annotations

from typing import Any, assert_type

from django import forms
from typing_extensions import override


# User-defined widgets may return any value usable in a template from `format_value`
class IntWidget(forms.Widget):
    @override
    def format_value(self, value: Any) -> int:
        return int(value)


def test_format_value_override(widget: IntWidget) -> None:
    assert_type(widget.format_value("1"), int)
