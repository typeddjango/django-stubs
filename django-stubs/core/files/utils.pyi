from typing import BinaryIO, Any, Optional, Tuple, Union

class FileProxyMixin(BinaryIO):

    newlines = ... # type: Union[str, Tuple[str, ...], None]
    softspace = ... # type: bool

    def readinto(self, b: Any) -> Optional[int]: ...
