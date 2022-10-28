from typing import Any, Optional, Type, TypeVar

from django.db.models import Model
from django.forms.models import BaseModelFormSet, ModelForm

_M = TypeVar("_M", bound=Model)
_ModelFormT = TypeVar("_ModelFormT", bound=ModelForm)

class BaseGenericInlineFormSet(BaseModelFormSet[_M, _ModelFormT]):
    instance: Any = ...
    rel_name: Any = ...
    save_as_new: Any = ...
    def __init__(
        self,
        data: Optional[Any] = ...,
        files: Optional[Any] = ...,
        instance: Optional[Any] = ...,
        save_as_new: bool = ...,
        prefix: Optional[Any] = ...,
        queryset: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def initial_form_count(self) -> int: ...
    @classmethod
    def get_default_prefix(cls) -> str: ...
    def save_new(self, form: Any, commit: bool = ...) -> _M: ...

def generic_inlineformset_factory(
    model: Type[_M],
    form: Type[_ModelFormT] = ...,
    formset: Any = ...,
    ct_field: str = ...,
    fk_field: str = ...,
    fields: Optional[Any] = ...,
    exclude: Optional[Any] = ...,
    extra: int = ...,
    can_order: bool = ...,
    can_delete: bool = ...,
    max_num: Optional[Any] = ...,
    formfield_callback: Optional[Any] = ...,
    validate_max: bool = ...,
    for_concrete_model: bool = ...,
    min_num: Optional[Any] = ...,
    validate_min: bool = ...,
    absolute_max: Optional[int] = ...,
    can_delete_extra: bool = ...,
) -> Type[BaseGenericInlineFormSet[_M, _ModelFormT]]: ...
