from __future__ import annotations

from typing import assert_type

from django.forms.renderers import DjangoTemplates, Jinja2, TemplatesSetting
from django.template.backends.django import Template as DjangoTemplate
from django.template.backends.jinja2 import Template as Jinja2Template
from django.utils.safestring import SafeString


def renderer_templates() -> None:
    assert_type(DjangoTemplates().get_template("a.html"), DjangoTemplate)
    assert_type(Jinja2().get_template("a.html"), Jinja2Template)
    assert_type(TemplatesSetting().get_template("a.html").render({}), str)
    assert_type(DjangoTemplates().get_template("a.html").render({}), SafeString)
