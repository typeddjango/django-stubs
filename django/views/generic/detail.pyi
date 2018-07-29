from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.template.response import TemplateResponse
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


class BaseDetailView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class SingleObjectMixin:
    def get_context_data(self, **kwargs) -> Dict[str, Any]: ...
    def get_context_object_name(self, obj: Union[Model, Dict[str, str]]) -> Optional[str]: ...
    def get_object(self, queryset: Optional[QuerySet] = ...) -> Model: ...
    def get_queryset(self) -> QuerySet: ...
    def get_slug_field(self) -> str: ...


class SingleObjectTemplateResponseMixin:
    def get_template_names(self) -> List[str]: ...