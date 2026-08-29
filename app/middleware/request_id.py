import re
from uuid import uuid4

from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-ID"
REQUEST_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
)


def resolve_request_id(candidate: str | None) -> str:
    """Reuse a valid request ID or generate a UUID v4 replacement."""
    if candidate is not None and REQUEST_ID_PATTERN.fullmatch(candidate):
        return candidate

    return str(uuid4())


class RequestIDMiddleware:
    """Attach a validated request ID to each HTTP request and response."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = resolve_request_id(
            Headers(scope=scope).get(REQUEST_ID_HEADER),
        )
        scope.setdefault("state", {})["request_id"] = request_id

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = MutableHeaders(scope=message)
                response_headers[REQUEST_ID_HEADER] = request_id

            await send(message)

        await self.app(scope, receive, send_with_request_id)
