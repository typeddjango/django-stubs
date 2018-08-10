from collections import OrderedDict
from datetime import date, datetime
from typing import Any, Dict, Iterator, List, Optional, Union

from django.core.serializers import base
from django.core.serializers.base import DeserializedObject
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Serializer(base.Serializer):
    options: Dict[Any, Any]
    selected_fields: None
    stream: _io.StringIO
    use_natural_foreign_keys: bool
    use_natural_primary_keys: bool
    internal_use_only: bool = ...
    objects: List[Any] = ...
    def start_serialization(self) -> None: ...
    def end_serialization(self) -> None: ...
    def start_object(self, obj: Model) -> None: ...
    def end_object(self, obj: Model) -> None: ...
    def get_dump_object(self, obj: Model) -> OrderedDict: ...
    def handle_field(self, obj: Model, field: Field) -> None: ...
    def handle_fk_field(self, obj: Model, field: ForeignKey) -> None: ...
    def handle_m2m_field(self, obj: Model, field: ManyToManyField) -> None: ...
    def getvalue(self) -> List[OrderedDict]: ...

def Deserializer(
    object_list: Union[
        List[
            Dict[
                str,
                Union[
                    Dict[str, Union[List[Any], List[int], datetime, int, str]],
                    int,
                    str,
                ],
            ]
        ],
        List[
            Union[
                Dict[str, Optional[Union[Dict[str, Optional[str]], str]]],
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[List[str]], List[str], str]],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str, Optional[Union[Dict[str, Union[float, int, str]], str]]
                ],
                Dict[str, Optional[Union[Dict[str, str], str]]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[Any, Any], date, str]],
                Dict[str, Union[Dict[Any, Any], float, str]],
                Dict[str, Union[Dict[Any, Any], int, str]],
                Dict[str, Union[Dict[str, List[Any]], int, str]],
                Dict[str, Union[Dict[str, List[int]], int, str]],
                Dict[str, Union[Dict[str, None], int, str]],
                Dict[str, Union[Dict[str, Union[List[Any], List[str]]], str]],
                Dict[
                    str,
                    Union[Dict[str, Union[List[List[str]], List[str]]], str],
                ],
                Dict[str, Union[Dict[str, Union[int, str]], int, str]],
                Dict[str, Union[Dict[str, bool], int, str]],
                Dict[str, Union[Dict[str, date], int, str]],
                Dict[str, Union[Dict[str, datetime], int, str]],
                Dict[str, Union[Dict[str, float], int, str]],
                Dict[str, Union[Dict[str, int], int, str]],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[str, List[Any]], int, str]],
                Dict[str, Union[Dict[str, Union[List[Any], str]], int, str]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[str, List[str]], int, str]],
                Dict[str, Union[Dict[str, None], int, str]],
                Dict[str, Union[Dict[str, Optional[str]], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[Any], List[List[str]], bool, str]],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, Union[List[Any], str]], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[Any], List[int], bool, str]],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, Union[List[Any], str]], int, str]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[str, Union[List[Any], str]], int, str]],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[List[str]], int, str]], int, str
                    ],
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str, Union[Dict[str, Union[List[List[str]], str]], int, str]
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[Union[int, str]], int, str]],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str,
                    Union[
                        Dict[str, Union[List[int], datetime, int, str]],
                        int,
                        str,
                    ],
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[
                    str, Union[Dict[str, Union[List[int], int, str]], int, str]
                ],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[str, Union[List[int], str]], int, str]],
                Dict[str, Union[Dict[str, str], int, str]],
            ]
        ],
        List[
            Union[
                Dict[str, Union[Dict[str, Union[List[str], str]], int, str]],
                Dict[str, Union[Dict[str, str], str]],
            ]
        ],
    ],
    *,
    using: Any = ...,
    ignorenonexistent: bool = ...,
    **options: Any
) -> Iterator[DeserializedObject]: ...
