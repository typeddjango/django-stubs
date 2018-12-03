from collections import OrderedDict
from decimal import Decimal
from typing import Any, Optional, Union

from yaml import CSafeDumper as SafeDumper
from yaml.nodes import MappingNode, ScalarNode

from django.core.serializers.python import Serializer as PythonSerializer
from django.db.models.base import Model
from django.db.models.fields import Field

class DjangoSafeDumper(SafeDumper):
    alias_key: int
    allow_unicode: None
    analysis: None
    anchors: Dict[Any, Any]
    best_indent: int
    best_line_break: str
    best_width: int
    canonical: None
    closed: bool
    column: int
    default_flow_style: None
    default_style: None
    encoding: None
    event: None
    events: List[Any]
    flow_level: int
    indent: None
    indention: bool
    indents: List[Any]
    last_anchor_id: int
    line: int
    mapping_context: bool
    object_keeper: List[Union[List[collections.OrderedDict], collections.OrderedDict, datetime.datetime]]
    open_ended: bool
    prepared_anchor: None
    prepared_tag: None
    represented_objects: Dict[int, Union[yaml.nodes.MappingNode, yaml.nodes.ScalarNode, yaml.nodes.SequenceNode]]
    resolver_exact_paths: List[Any]
    resolver_prefix_paths: List[Any]
    root_context: bool
    sequence_context: bool
    serialized_nodes: Dict[Any, Any]
    simple_key_context: bool
    state: Callable
    states: List[Any]
    stream: _io.StringIO
    style: None
    tag_prefixes: None
    use_encoding: None
    use_explicit_end: None
    use_explicit_start: None
    use_tags: None
    use_version: None
    whitespace: bool
    def represent_decimal(self, data: Decimal) -> ScalarNode: ...
    def represent_ordered_dict(self, data: OrderedDict) -> MappingNode: ...

class Serializer(PythonSerializer):
    objects: List[Any]
    options: Dict[Any, Any]
    selected_fields: None
    stream: _io.StringIO
    use_natural_foreign_keys: bool
    use_natural_primary_keys: bool
    internal_use_only: bool = ...
    def handle_field(self, obj: Model, field: Field) -> None: ...
    def end_serialization(self) -> None: ...
    def getvalue(self) -> Union[bytes, str]: ...

def Deserializer(stream_or_string: str, **options: Any) -> None: ...
