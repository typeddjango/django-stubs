from datetime import date
from django.template.base import NodeList
from django.template.context import Context
from django.utils.safestring import SafeText


def unlocalize(value: date) -> str: ...


class LocalizeNode:
    def __init__(self, nodelist: NodeList, use_l10n: bool) -> None: ...
    def render(self, context: Context) -> SafeText: ...