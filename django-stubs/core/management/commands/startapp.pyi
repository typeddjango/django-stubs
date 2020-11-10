from django.core.management.templates import TemplateCommand as TemplateCommand
from typing import Any

class Command(TemplateCommand):
    missing_args_message: str = ...
