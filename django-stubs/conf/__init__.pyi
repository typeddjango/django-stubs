from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.utils.functional import LazyObject

ENVIRONMENT_VARIABLE: str

class LazySettings(LazyObject):
    def __getattr__(
        self, name: str
    ) -> Optional[
        Union[
            Callable,
            Dict[int, None],
            Dict[int, str],
            Dict[str, Callable],
            Dict[
                str,
                Optional[
                    Union[
                        Dict[str, Union[Callable, Dict[str, int], str]],
                        Dict[str, Union[Dict[str, int], int, str]],
                    ]
                ],
            ],
            Dict[str, Optional[str]],
            Dict[
                str,
                Union[
                    Dict[
                        str,
                        Optional[
                            Union[Dict[Any, Any], Dict[str, None], int, str]
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
                            Dict[str, Union[List[str], bool, str]],
                            Dict[str, Union[List[str], str]],
                        ],
                    ],
                    Dict[
                        str,
                        Union[Dict[str, Union[List[str], str]], Dict[str, str]],
                    ],
                    int,
                    str,
                ],
            ],
            List[Dict[str, Union[Dict[str, List[Any]], List[Any], bool, str]]],
            List[Dict[str, Union[Dict[str, Tuple[str]], List[str], str]]],
            List[
                Union[
                    Dict[str, Union[Dict[Any, Any], bool, str]],
                    Dict[str, Union[Dict[str, bool], bool, str]],
                ]
            ],
            List[
                Union[
                    Dict[
                        str,
                        Union[Dict[str, List[Tuple[str, Dict[str, str]]]], str],
                    ],
                    Dict[str, Union[Dict[str, int], str]],
                ]
            ],
            List[
                Union[
                    Dict[
                        str, Union[Dict[str, List[str]], List[str], bool, str]
                    ],
                    Dict[
                        str,
                        Union[Dict[str, Tuple[str, str]], List[str], bool, str],
                    ],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[Dict[str, bool], str]],
                    Dict[str, Union[Dict[str, int], str]],
                ]
            ],
            List[
                Union[
                    Dict[str, Union[Dict[str, int], str]],
                    Dict[str, Union[Dict[str, str], str]],
                ]
            ],
            List[Union[Tuple[str, str], str]],
            List[int],
            Tuple[Tuple[str, str], Tuple[str, str]],
            Tuple[str, str],
            Type[Any],
            float,
            int,
            str,
        ]
    ]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def configure(self, default_settings: Any = ..., **options: Any) -> Any: ...
    @property
    def configured(self) -> bool: ...

class Settings:
    FORCE_SCRIPT_NAME: None
    INSTALLED_APPS: List[Any]
    LOGGING: Dict[Any, Any]
    LOGGING_CONFIG: str
    SETTINGS_MODULE: Any = ...
    def __init__(self, settings_module: str) -> None: ...
    def is_overridden(self, setting: str) -> bool: ...

class UserSettingsHolder:
    SETTINGS_MODULE: Any = ...
    default_settings: django.conf.Settings = ...
    def __init__(
        self, default_settings: Union[Settings, UserSettingsHolder]
    ) -> None: ...
    def __getattr__(
        self, name: str
    ) -> Optional[
        Union[
            Dict[
                str,
                Dict[
                    str,
                    Optional[Union[Dict[Any, Any], Dict[str, None], int, str]],
                ],
            ],
            Dict[
                str,
                Optional[
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], bool, str]],
                                Dict[str, Union[List[str], str]],
                            ],
                        ],
                        Dict[
                            str,
                            Union[
                                Dict[str, Union[List[str], str]], Dict[str, str]
                            ],
                        ],
                        int,
                    ]
                ],
            ],
            Dict[str, str],
            List[Dict[str, Union[Dict[str, List[str]], List[str], bool, str]]],
            List[Dict[str, Union[Dict[str, Tuple[str]], List[str], bool, str]]],
            List[Union[Tuple[str, str], str]],
            List[int],
            float,
            int,
            str,
        ]
    ]: ...
    def __setattr__(
        self,
        name: str,
        value: Optional[
            Union[
                Callable,
                Dict[int, None],
                Dict[int, str],
                Dict[str, Callable],
                Dict[
                    str,
                    Optional[
                        Union[
                            Dict[str, Dict[str, Union[List[str], bool, str]]],
                            int,
                        ]
                    ],
                ],
                Dict[str, Optional[str]],
                Dict[str, Union[Dict[str, Optional[str]], str]],
                Dict[
                    str,
                    Union[
                        Dict[str, Union[Callable, Dict[str, int], str]],
                        Dict[str, Union[Dict[str, int], int, str]],
                    ],
                ],
                List[
                    Dict[str, Union[Dict[str, List[Any]], List[Any], bool, str]]
                ],
                List[Dict[str, Union[Dict[str, Tuple[str]], List[str], str]]],
                List[
                    Union[
                        Dict[str, Union[Dict[Any, Any], bool, str]],
                        Dict[str, Union[Dict[str, bool], bool, str]],
                    ]
                ],
                List[
                    Union[
                        Dict[
                            str,
                            Union[
                                Dict[str, List[Tuple[str, Dict[str, str]]]], str
                            ],
                        ],
                        Dict[str, Union[Dict[str, int], str]],
                    ]
                ],
                List[
                    Union[
                        Dict[
                            str,
                            Union[Dict[str, List[str]], List[str], bool, str],
                        ],
                        Dict[
                            str,
                            Union[
                                Dict[str, Tuple[str, str]], List[str], bool, str
                            ],
                        ],
                    ]
                ],
                List[
                    Union[
                        Dict[str, Union[Dict[str, bool], str]],
                        Dict[str, Union[Dict[str, int], str]],
                    ]
                ],
                List[
                    Union[
                        Dict[str, Union[Dict[str, int], str]],
                        Dict[str, Union[Dict[str, str], str]],
                    ]
                ],
                List[Union[Tuple[str, str], str]],
                List[int],
                Tuple[Tuple[str, str], Tuple[str, str]],
                Tuple[str],
                Type[Any],
                bytes,
                Settings,
                UserSettingsHolder,
                float,
                int,
                str,
            ]
        ],
    ) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __dir__(self) -> List[str]: ...
    def is_overridden(self, setting: str) -> bool: ...

settings: Any
