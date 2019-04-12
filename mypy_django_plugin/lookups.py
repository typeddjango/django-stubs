from typing import List, Union

import dataclasses
from mypy.nodes import TypeInfo
from mypy.plugin import CheckerPluginInterface
from mypy.types import Instance, Type

from mypy_django_plugin import helpers


@dataclasses.dataclass
class RelatedModelNode:
    typ: Instance
    is_nullable: bool


@dataclasses.dataclass
class FieldNode:
    typ: Type


LookupNode = Union[RelatedModelNode, FieldNode]


class LookupException(Exception):
    pass


def resolve_lookup(api: CheckerPluginInterface, model_type_info: TypeInfo, lookup: str) -> List[LookupNode]:
    """Resolve a lookup str to a list of LookupNodes.

    Each node represents a part of the lookup (separated by "__"), in order.
    Each node is the Model or Field that was resolved.

    Raises LookupException if there were any issues resolving the lookup.
    """
    lookup_parts = lookup.split("__")

    nodes = []
    while lookup_parts:
        lookup_part = lookup_parts.pop(0)

        if not nodes:
            current_node = None
        else:
            current_node = nodes[-1]

        if current_node is None:
            new_node = resolve_model_lookup(api, model_type_info, lookup_part)
        elif isinstance(current_node, RelatedModelNode):
            new_node = resolve_model_lookup(api, current_node.typ.type, lookup_part)
        elif isinstance(current_node, FieldNode):
            raise LookupException(f"Field lookups not yet supported for lookup {lookup}")
        else:
            raise LookupException(f"Unsupported node type: {type(current_node)}")
        nodes.append(new_node)
    return nodes


def resolve_model_pk_lookup(api: CheckerPluginInterface, model_type_info: TypeInfo) -> LookupNode:
    # Primary keys are special-cased
    primary_key_type = helpers.extract_primary_key_type_for_get(model_type_info)
    if primary_key_type:
        return FieldNode(primary_key_type)
    else:
        # No PK, use the get type for AutoField as PK type.
        autofield_info = api.lookup_typeinfo('django.db.models.fields.AutoField')
        pk_type = helpers.get_private_descriptor_type(autofield_info, '_pyi_private_get_type',
                                                      is_nullable=False)
        return FieldNode(pk_type)


def resolve_model_lookup(api: CheckerPluginInterface, model_type_info: TypeInfo,
                         lookup: str) -> LookupNode:
    """Resolve a lookup on the given model."""
    if lookup == 'pk':
        return resolve_model_pk_lookup(api, model_type_info)

    field_name = get_actual_field_name_for_lookup_field(lookup, model_type_info)

    field_node = model_type_info.get(field_name)
    if not field_node:
        raise LookupException(
            f'When resolving lookup "{lookup}", field "{field_name}" was not found in model {model_type_info.name()}')

    if field_name.endswith('_id'):
        field_name_without_id = field_name.rstrip('_id')
        foreign_key_field = model_type_info.get(field_name_without_id)
        if foreign_key_field is not None and helpers.is_foreign_key_like(foreign_key_field.type):
            # Hack: If field ends with '_id' and there is a model field without the '_id' suffix, then use that field.
            field_node = foreign_key_field
            field_name = field_name_without_id

    field_node_type = field_node.type
    if field_node_type is None or not isinstance(field_node_type, Instance):
        raise LookupException(
            f'When resolving lookup "{lookup}", could not determine type for {model_type_info.name()}.{field_name}')

    if field_node_type.type.fullname() == 'builtins.object':
        # could be related manager
        related_manager_type = helpers.get_related_manager_type_from_metadata(model_type_info, field_name, api)
        if related_manager_type:
            model_arg = related_manager_type.args[0]
            if not isinstance(model_arg, Instance):
                raise LookupException(
                    f'When resolving lookup "{lookup}", could not determine type '
                    f'for {model_type_info.name()}.{field_name}')

            return RelatedModelNode(typ=model_arg, is_nullable=False)

    if helpers.is_foreign_key_like(field_node_type):
        field_type = helpers.extract_field_getter_type(field_node_type)
        is_nullable = helpers.is_optional(field_type)
        if is_nullable:
            # type is always non-optional
            field_type = helpers.make_required(field_type)

        if isinstance(field_type, Instance):
            return RelatedModelNode(typ=field_type, is_nullable=is_nullable)
        else:
            raise LookupException(f"Not an instance for field {field_type} lookup {lookup}")

    field_type = helpers.extract_field_getter_type(field_node_type)
    if field_type:
        return FieldNode(typ=field_type)

    # Not a Field
    if field_name == 'id':
        # If no 'id' field was found, use an int
        return FieldNode(api.named_generic_type('builtins.int', []))

    raise LookupException(
        f'When resolving lookup {lookup!r}, could not determine type for {model_type_info.name()}.{field_name}')


def get_actual_field_name_for_lookup_field(lookup: str, model_type_info: TypeInfo) -> str:
    """Attempt to find out the real field name if this lookup is a related_query_name (for reverse relations).

    If it's not, return the original lookup.
    """
    lookups_metadata = helpers.get_lookups_metadata(model_type_info)
    lookup_metadata = lookups_metadata.get(lookup)
    if lookup_metadata is None:
        # If not found on current model, look in all bases for their lookup metadata
        for base in model_type_info.mro:
            lookups_metadata = helpers.get_lookups_metadata(base)
            lookup_metadata = lookups_metadata.get(lookup)
            if lookup_metadata:
                break
    if not lookup_metadata:
        lookup_metadata = {}
    related_name = lookup_metadata.get('related_query_name_target', None)
    if related_name:
        # If the lookup is a related lookup, then look at the field specified by related_name.
        # This is to support if related_query_name is set and differs from.
        field_name = related_name
    else:
        field_name = lookup
    return field_name
