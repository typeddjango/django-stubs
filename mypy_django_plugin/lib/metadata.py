from typing import Any, Dict, List

from mypy.nodes import TypeInfo


def get_django_metadata(model_info: TypeInfo) -> Dict[str, Any]:
    return model_info.metadata.setdefault('django', {})


def get_related_field_primary_key_names(base_model: TypeInfo) -> List[str]:
    return get_django_metadata(base_model).setdefault('related_field_primary_keys', [])


def get_fields_metadata(model: TypeInfo) -> Dict[str, Any]:
    return get_django_metadata(model).setdefault('fields', {})


def get_lookups_metadata(model: TypeInfo) -> Dict[str, Any]:
    return get_django_metadata(model).setdefault('lookups', {})


def get_related_managers_metadata(model: TypeInfo) -> Dict[str, Any]:
    return get_django_metadata(model).setdefault('related_managers', {})
