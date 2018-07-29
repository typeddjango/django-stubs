from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.fields import (
    BooleanField,
    DateField,
    Field,
)
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
)
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.query import QuerySet
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


class AllValuesFieldListFilter:
    def __init__(
        self,
        field: Field,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    def expected_parameters(self) -> List[str]: ...


class BooleanFieldListFilter:
    def __init__(
        self,
        field: BooleanField,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    def expected_parameters(self) -> List[str]: ...


class ChoicesFieldListFilter:
    def __init__(
        self,
        field: Field,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    def expected_parameters(self) -> List[str]: ...


class DateFieldListFilter:
    def __init__(
        self,
        field: DateField,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    def expected_parameters(self) -> List[str]: ...


class FieldListFilter:
    def __init__(
        self,
        field: Union[ForeignObjectRel, Field],
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    @classmethod
    def create(
        cls,
        field: Union[ForeignObjectRel, Field],
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> FieldListFilter: ...
    def has_output(self) -> bool: ...
    def queryset(
        self,
        request: WSGIRequest,
        queryset: QuerySet
    ) -> QuerySet: ...
    @classmethod
    def register(
        cls,
        test: Callable,
        list_filter_class: Type[FieldListFilter],
        take_priority: bool = ...
    ) -> None: ...


class ListFilter:
    def __init__(
        self,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin
    ) -> None: ...


class RelatedFieldListFilter:
    def __init__(
        self,
        field: Union[ForeignObjectRel, ManyToManyField, ForeignKey],
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin,
        field_path: str
    ) -> None: ...
    def expected_parameters(self) -> List[str]: ...
    def field_choices(
        self,
        field: Union[ForeignObjectRel, ManyToManyField, ForeignKey],
        request: WSGIRequest,
        model_admin: ModelAdmin
    ) -> Union[List[Tuple[str, str]], List[Tuple[int, str]]]: ...
    def has_output(self) -> bool: ...
    @property
    def include_empty_choice(self) -> bool: ...


class RelatedOnlyFieldListFilter:
    def field_choices(
        self,
        field: Union[ManyToManyField, ForeignKey],
        request: WSGIRequest,
        model_admin: ModelAdmin
    ) -> Union[List[Tuple[str, str]], List[Tuple[int, str]]]: ...


class SimpleListFilter:
    def __init__(
        self,
        request: WSGIRequest,
        params: Dict[str, str],
        model: Type[Model],
        model_admin: ModelAdmin
    ) -> None: ...
    def has_output(self) -> bool: ...
    def value(self) -> Optional[str]: ...