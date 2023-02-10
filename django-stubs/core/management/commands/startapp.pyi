from django.core.management.templates import TemplateCommand

class Command(TemplateCommand):
    missing_args_message: str
