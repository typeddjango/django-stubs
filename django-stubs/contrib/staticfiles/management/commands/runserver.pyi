from django.contrib.staticfiles.handlers import StaticFilesHandler

class Command:
    def get_handler(self, *args, **options) -> StaticFilesHandler: ...
