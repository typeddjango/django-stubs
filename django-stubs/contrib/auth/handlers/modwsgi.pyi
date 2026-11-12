from typing import Any
from wsgiref.types import WSGIEnvironment

UserModel: Any

def check_password(environ: WSGIEnvironment, username: str, password: str) -> bool | None: ...
def groups_for_user(environ: WSGIEnvironment, username: str) -> list[bytes]: ...
