from __future__ import annotations

from typing import Any

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application


class Router:
    async def __call__(self, scope: Any, receive: Any, send: Any) -> None: ...


ASGIStaticFilesHandler(get_asgi_application())
# any ASGI application, e.g. channels' ProtocolTypeRouter
ASGIStaticFilesHandler(Router())
