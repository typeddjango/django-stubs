from typing import Any, Optional, Tuple, Type, Union

from django.db.models.base import Model

def make_model_tuple(model: Union[Type[Model], str]) -> Tuple[str, str]: ...
