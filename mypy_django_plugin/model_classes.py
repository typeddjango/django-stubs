import json
from typing import Dict

import dataclasses


@dataclasses.dataclass
class ModelInfo(object):
    # class_name: str
    related_managers: Dict[str, 'ModelInfo'] = dataclasses.field(default_factory=dict)


def get_default_base_models():
    return {'django.db.models.base.Model': ModelInfo()}


@dataclasses.dataclass
class DjangoModelsRegistry(object):
    base_models: Dict[str, ModelInfo] = dataclasses.field(default_factory=get_default_base_models)

    def __contains__(self, item: str) -> bool:
        return item in self.base_models
