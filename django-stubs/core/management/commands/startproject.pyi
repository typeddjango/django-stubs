from ..utils import get_random_secret_key as get_random_secret_key
from django.core.management.templates import TemplateCommand as TemplateCommand

class Command(TemplateCommand):
    missing_args_message: str = ...
