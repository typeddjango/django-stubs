from django.core.mail.message import EmailMessage
from typing import List


class EmailBackend:
    def send_messages(self, email_messages: List[EmailMessage]) -> int: ...