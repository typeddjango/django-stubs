from typing import Any, Dict, List, Optional, Type

from django.db import models
from django.http import HttpResponse, HttpRequest
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View

class SingleObjectMixin(ContextMixin):
    model = ...  # type: Optional[Type[models.Model]]
    queryset = ...  # type: Optional[models.query.QuerySet]
    slug_field = ...  # type: str
    context_object_name = ...  # type: Optional[str]
    slug_url_kwarg = ...  # type: str
    pk_url_kwarg = ...  # type: str
    query_pk_and_slug = ...  # type: bool
    object = ...  # type: models.Model
    kwargs = ...  # type: Dict[str, object]
    def get_object(self, queryset: models.query.QuerySet = None) -> models.Model: ...
    def get_queryset(self) -> models.query.QuerySet: ...
    def get_slug_field(self) -> str: ...
    def get_context_object_name(self, obj: Any) -> Optional[str]: ...
    def get_context_data(self, **kwargs: object) -> Dict[str, object]: ...

class BaseDetailView(SingleObjectMixin, View):
    def render_to_response(self, context: Dict[str, object], **response_kwargs: object) -> HttpResponse: ...
    object = ...  # type: models.Model
    def get(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse: ...

class SingleObjectTemplateResponseMixin(TemplateResponseMixin):
    template_name_field = ...  # type: Optional[str]
    template_name_suffix = ...  # type: str
    model = ...  # type: Optional[Type[models.Model]]
    object = ...  # type: models.Model
    def get_template_names(self) -> List[str]: ...

class DetailView(SingleObjectTemplateResponseMixin, BaseDetailView): ...
