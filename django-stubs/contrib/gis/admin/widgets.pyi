from django.forms.widgets import Textarea as Textarea
from typing import Any

geo_context: Any
logger: Any

class OpenLayersWidget(Textarea):
    def get_context(self, name: Any, value: Any, attrs: Any): ...
    def map_options(self): ...
