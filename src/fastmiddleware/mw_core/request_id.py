"""Inject a per-request correlation id (header + ContextVar)."""

from __future__ import annotations

import uuid
from typing import Callable, Optional

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from core.utils.request_id_context import RequestIdContext

DEFAULT_REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Set ``X-Request-ID`` on the response and bind the value to ``fast_platform`` request id context.

    If the client sends the header and ``accept_incoming`` is True, that value is reused;
    otherwise a new UUID4 string is generated.
    """

    def __init__(
        self,
        app,
        *,
        header_name: str = DEFAULT_REQUEST_ID_HEADER,
        accept_incoming: bool = True,
        id_factory: Optional[Callable[[], str]] = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            header_name: The header_name parameter.
            accept_incoming: The accept_incoming parameter.
            id_factory: The id_factory parameter.
        """
        super().__init__(app)
        self.header_name = header_name
        self.accept_incoming = accept_incoming
        self._id_factory = id_factory or (lambda: str(uuid.uuid4()))

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        if self.accept_incoming:
            raw = request.headers.get(self.header_name)
            incoming = (raw or "").strip()
            rid = incoming if incoming else self._id_factory()
        else:
            rid = self._id_factory()
        token = RequestIdContext.set(rid)
        try:
            response = await call_next(request)
            response.headers[self.header_name] = rid
            return response
        finally:
            RequestIdContext.reset(token)
