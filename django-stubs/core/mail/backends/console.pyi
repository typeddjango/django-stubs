import threading
from typing import TextIO

from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    stream: TextIO
    _lock: threading.RLock
