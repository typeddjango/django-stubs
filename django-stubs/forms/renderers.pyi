from datetime import time
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from django.template.backends.base import BaseEngine
from django.template.backends.django import Template
from django.template.backends.jinja2 import Template

ROOT: Any

def get_default_renderer() -> DjangoTemplates: ...

class BaseRenderer:
    def get_template(self, template_name: str) -> Any: ...
    def render(
        self,
        template_name: str,
        context: Union[
            Dict[
                str,
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[str, Union[bool, Decimal, str]],
                            List[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[Any, Any], bool, time, str
                                            ],
                                        ]
                                    ],
                                    int,
                                ]
                            ],
                            bool,
                            str,
                        ]
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[str, Union[bool, str]],
                            List[
                                Union[
                                    Dict[
                                        str,
                                        Optional[
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                List[
                                                    Dict[
                                                        str,
                                                        Optional[
                                                            Union[
                                                                Dict[
                                                                    str,
                                                                    Union[
                                                                        bool,
                                                                        str,
                                                                    ],
                                                                ],
                                                                bool,
                                                                str,
                                                            ]
                                                        ],
                                                    ]
                                                ],
                                                bool,
                                                str,
                                            ]
                                        ],
                                    ],
                                    Dict[
                                        str,
                                        Optional[
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                bool,
                                                str,
                                            ]
                                        ],
                                    ],
                                    Dict[
                                        str,
                                        Union[
                                            Dict[str, Union[bool, str]],
                                            List[Any],
                                            List[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[Any, Any],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ]
                                            ],
                                            bool,
                                            str,
                                        ],
                                    ],
                                ]
                            ],
                            bool,
                            str,
                        ]
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[str, Union[float, int, str]],
                            List[
                                Dict[
                                    str,
                                    Optional[Union[Dict[str, str], bool, str]],
                                ]
                            ],
                            bool,
                            str,
                        ]
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[Any, Any],
                        List[
                            Dict[
                                str,
                                Union[
                                    Dict[Any, Any],
                                    List[
                                        Union[
                                            Tuple[
                                                None,
                                                List[
                                                    Dict[
                                                        str,
                                                        Union[
                                                            Dict[Any, Any],
                                                            bool,
                                                            str,
                                                        ],
                                                    ]
                                                ],
                                                int,
                                            ],
                                            Tuple[
                                                None,
                                                List[
                                                    Dict[
                                                        str,
                                                        Union[
                                                            Dict[str, bool],
                                                            bool,
                                                            str,
                                                        ],
                                                    ]
                                                ],
                                                int,
                                            ],
                                        ]
                                    ],
                                    List[str],
                                    bool,
                                    str,
                                ],
                            ]
                        ],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[Any, Any],
                        List[
                            Tuple[
                                None,
                                List[
                                    Dict[
                                        str,
                                        Union[Dict[Any, Any], bool, time, str],
                                    ]
                                ],
                                int,
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[Any, Any],
                        List[
                            Union[
                                Dict[
                                    str,
                                    Union[
                                        Dict[Any, Any],
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        bool,
                                        str,
                                    ],
                                ],
                                Dict[str, Union[Dict[Any, Any], bool, str]],
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, bool],
                                        List[
                                            Union[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[Any, Any],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ],
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[str, bool],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ],
                                            ]
                                        ],
                                        List[str],
                                        bool,
                                        str,
                                    ],
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Tuple[
                                None,
                                List[
                                    Dict[str, Union[Dict[str, str], int, str]]
                                ],
                                int,
                            ]
                        ],
                        List[
                            Union[
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, Union[bool, str]],
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    bool,
                                                    str,
                                                ],
                                            ]
                                        ],
                                        bool,
                                        str,
                                    ],
                                ],
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, Union[bool, str]],
                                        List[
                                            Union[
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[Any, Any],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ],
                                                Tuple[
                                                    None,
                                                    List[
                                                        Dict[
                                                            str,
                                                            Union[
                                                                Dict[str, bool],
                                                                bool,
                                                                str,
                                                            ],
                                                        ]
                                                    ],
                                                    int,
                                                ],
                                            ]
                                        ],
                                        List[str],
                                        bool,
                                        str,
                                    ],
                                ],
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, Union[bool, str]], bool, str
                                    ],
                                ],
                            ]
                        ],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Tuple[
                                None,
                                List[
                                    Union[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ],
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, bool],
                                                Set[str],
                                                int,
                                                str,
                                            ],
                                        ],
                                    ]
                                ],
                                int,
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str, Union[Dict[Any, Any], int, str]
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], int, str],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                bool,
                                                str,
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                int,
                                                str,
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                bool,
                                                str,
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, str], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[int, str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str, Union[Dict[Any, Any], int, str]
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, Union[int, str]],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, str], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    str,
                                    List[
                                        Union[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    bool,
                                                    str,
                                                ],
                                            ],
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, str], bool, str
                                                ],
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        int,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, bool],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, bool],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    str,
                                    List[
                                        Union[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ],
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, bool], bool, str
                                                ],
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, str],
                        List[Dict[str, Union[Dict[str, str], bool, str]]],
                        List[int],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, str],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[Any, Any], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, bool], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Dict[
                    str,
                    Union[
                        Dict[str, str],
                        List[
                            Union[
                                Tuple[
                                    None,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, str], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    str,
                                    List[
                                        Dict[
                                            str,
                                            Union[Dict[str, str], bool, str],
                                        ]
                                    ],
                                    int,
                                ],
                                Tuple[
                                    str,
                                    List[
                                        Union[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, Union[bool, str]],
                                                    bool,
                                                    str,
                                                ],
                                            ],
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, str], bool, str
                                                ],
                                            ],
                                        ]
                                    ],
                                    int,
                                ],
                            ]
                        ],
                        List[str],
                        bool,
                        str,
                    ],
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[
                                Dict[Any, Any],
                                List[
                                    Dict[
                                        str,
                                        Optional[
                                            Union[Dict[Any, Any], bool, str]
                                        ],
                                    ]
                                ],
                                bool,
                                str,
                            ]
                        ],
                    ],
                    List[Dict[str, str]],
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[
                                Dict[str, Union[bool, str]],
                                List[
                                    Dict[
                                        str,
                                        Optional[
                                            Union[
                                                Dict[str, Union[bool, str]],
                                                bool,
                                                str,
                                            ]
                                        ],
                                    ]
                                ],
                                bool,
                                str,
                            ]
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[
                                Dict[str, str],
                                List[
                                    Dict[
                                        str,
                                        Optional[
                                            Union[Dict[str, str], bool, str]
                                        ],
                                    ]
                                ],
                                bool,
                                str,
                            ]
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[str, Optional[Union[Dict[str, str], bool, str]]],
                    List[Dict[str, str]],
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[Dict[str, Union[Dict[str, str], bool, str]]],
                            bool,
                            str,
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[Any, Any],
                            List[
                                Union[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        str,
                                        List[
                                            Union[
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[Any, Any],
                                                        bool,
                                                        str,
                                                    ],
                                                ],
                                                Dict[
                                                    str,
                                                    Union[
                                                        Dict[str, bool],
                                                        bool,
                                                        str,
                                                    ],
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[
                                Dict[
                                    str,
                                    Union[
                                        Dict[str, Union[bool, str]], bool, str
                                    ],
                                ]
                            ],
                            bool,
                            str,
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[str, Union[bool, str]],
                            List[
                                Union[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, bool], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                    Tuple[
                                        str,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[Any, Any], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ],
                                ]
                            ],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Union[
                            Dict[str, str],
                            List[Dict[str, Union[Dict[str, str], bool, str]]],
                            List[str],
                            bool,
                            str,
                        ],
                    ],
                    str,
                ],
            ],
            Dict[str, Union[bool, str]],
        ],
        request: None = ...,
    ) -> str: ...

class EngineMixin:
    def get_template(self, template_name: str) -> Union[Template, Template]: ...
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    engine: django.template.backends.django.DjangoTemplates
    backend: Any = ...

class Jinja2(EngineMixin, BaseRenderer):
    engine: django.template.backends.jinja2.Jinja2
    backend: Any = ...

class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template: ...
