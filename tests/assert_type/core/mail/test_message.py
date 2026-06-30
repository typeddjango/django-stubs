from __future__ import annotations

from email.message import EmailMessage as StdlibEmailMessage
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from typing import Any

from django.core.mail.message import EmailMessage
from typing_extensions import assert_type

message = EmailMessage()
assert_type(message, EmailMessage)
assert_type(message.message(), StdlibEmailMessage)

message.attach("myfilename", "mycontent", "text/plain")

mime_text = MIMEText("mytext")
assert_type(mime_text, MIMEText)
message.attach(mime_text)

mime_image = MIMEImage(b"mydata", "png")
assert_type(mime_image, MIMEImage)
message.attach(mime_image)
assert_type(message.attachments, list[Any])
