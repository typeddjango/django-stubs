from collections.abc import Sequence

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

class EmailBackend(BaseEmailBackend):
    def send_messages(self, messages: Sequence[EmailMessage]) -> int: ...
