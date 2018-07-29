from typing import (
    Dict,
    Optional,
)


class SimplerXMLGenerator:
    def addQuickElement(
        self,
        name: str,
        contents: Optional[str] = ...,
        attrs: Optional[Dict[str, str]] = ...
    ) -> None: ...
    def characters(self, content: str) -> None: ...
    def startElement(self, name: str, attrs: Dict[str, str]) -> None: ...