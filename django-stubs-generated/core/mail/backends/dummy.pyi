from typing import Any, List, Optional

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

class EmailBackend(BaseEmailBackend):
    fail_silently: bool
    def send_messages(self, email_messages: List[EmailMessage]) -> int: ...
