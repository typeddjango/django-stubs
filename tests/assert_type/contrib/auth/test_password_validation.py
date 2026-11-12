from __future__ import annotations

from pathlib import PurePosixPath

from django.contrib.auth.password_validation import CommonPasswordValidator

# Runtime passes the path straight to `open()`, so any path-like works
CommonPasswordValidator(password_list_path=PurePosixPath("passwords.txt"))
