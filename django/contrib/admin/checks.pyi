from django.contrib.admin.options import (
    BaseModelAdmin,
    InlineModelAdmin,
    ModelAdmin,
    TabularInline,
)
from django.contrib.auth.models import (
    Group,
    User,
)
from django.core.checks.messages import Error
from django.db.models.base import Model
from typing import (
    Any,
    List,
    Tuple,
    Type,
    Union,
)


class BaseModelAdminChecks:
    def _check_autocomplete_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_autocomplete_fields_item(
        self,
        obj: Union[ModelAdmin, InlineModelAdmin],
        model: Type[Model],
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_exclude(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_field_spec(
        self,
        obj: BaseModelAdmin,
        model: Any,
        fields: Union[str, Tuple[str, str, str, str], Tuple[str, str]],
        label: str
    ) -> List[Any]: ...
    def _check_field_spec_item(
        self,
        obj: BaseModelAdmin,
        model: Any,
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_fieldsets(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_fieldsets_item(
        self,
        obj: BaseModelAdmin,
        model: Any,
        fieldset: Any,
        label: str,
        seen_fields: List[str]
    ) -> List[Any]: ...
    def _check_filter_horizontal(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_filter_item(
        self,
        obj: ModelAdmin,
        model: Type[Union[Group, User]],
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_filter_vertical(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_form(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_ordering(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_ordering_item(
        self,
        obj: ModelAdmin,
        model: Any,
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_prepopulated_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_prepopulated_fields_key(
        self,
        obj: Union[ModelAdmin, InlineModelAdmin],
        model: Type[Model],
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_prepopulated_fields_value(
        self,
        obj: BaseModelAdmin,
        model: Type[Model],
        val: Union[Tuple[str], List[str]],
        label: str
    ) -> List[Any]: ...
    def _check_prepopulated_fields_value_item(
        self,
        obj: Union[ModelAdmin, TabularInline],
        model: Type[Model],
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_radio_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_raw_id_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_raw_id_fields_item(
        self,
        obj: ModelAdmin,
        model: Type[Model],
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_readonly_fields(self, obj: BaseModelAdmin) -> List[Any]: ...
    def _check_readonly_fields_item(
        self,
        obj: BaseModelAdmin,
        model: Any,
        field_name: str,
        label: str
    ) -> List[Any]: ...
    def _check_view_on_site_url(self, obj: BaseModelAdmin) -> List[Any]: ...
    def check(
        self,
        admin_obj: BaseModelAdmin,
        **kwargs
    ) -> List[Error]: ...


class InlineModelAdminChecks:
    def _check_exclude_of_parent_model(
        self,
        obj: InlineModelAdmin,
        parent_model: Any
    ) -> List[Any]: ...
    def _check_extra(self, obj: InlineModelAdmin) -> List[Any]: ...
    def _check_formset(self, obj: InlineModelAdmin) -> List[Any]: ...
    def _check_has_add_permission(self, obj: InlineModelAdmin) -> None: ...
    def _check_max_num(self, obj: InlineModelAdmin) -> List[Any]: ...
    def _check_min_num(self, obj: InlineModelAdmin) -> List[Any]: ...
    def _check_relation(self, obj: InlineModelAdmin, parent_model: Any) -> List[Any]: ...