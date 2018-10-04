from typing import Set

import dataclasses


def get_default_base_models():
    return {'django.db.models.base.Model'}


@dataclasses.dataclass
class DjangoModelsRegistry(object):
    base_models: Set[str] = dataclasses.field(default_factory=get_default_base_models)

    def __contains__(self, item: str) -> bool:
        return item in self.base_models

    def __iter__(self):
        return iter(self.base_models)
