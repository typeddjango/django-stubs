from typing import Any, List, Optional

class CheckFieldDefaultMixin:
    def check(self, **kwargs: Any) -> List[Any]: ...
