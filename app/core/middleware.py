"""
Production middleware stack.

1. CorrelationIDMiddleware  — injects / generates X-Request-ID into every
   request context, log record, and active OTEL span.
2. RequestLoggingMiddleware — structured access log with latency, status,
   and correlation ID on every response.
"""
import time
import uuid
import logging
from contextvars import ContextVar

from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

# ── Context var so downstream code can read the request ID ───────────────────
REQUEST_ID_CTX: ContextVar[str] = ContextVar("request_id", default="")

REQUEST_ID_HEADER = "X-Request-ID"


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Reads X-Request-ID from the incoming request (set by load balancer / client).
    Generates a UUID4 if absent.
    Injects into:
      - The active OTEL span (request_id attribute)
      - The response header (X-Request-ID)
      - A ContextVar for use in structured logs
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        REQUEST_ID_CTX.set(request_id)

        # Attach to current OTEL span so it appears in traces
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("request_id", request_id)

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Structured access log — one line per request.
    Skips health/metrics probes to avoid log spam in production.
    """

    _SKIP_PATHS = frozenset(["/health", "/health/ready", "/metrics"])

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in self._SKIP_PATHS:
            return await call_next(request)

        t0 = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - t0) * 1000, 2)

        logger.info(
            "http_request",
            extra={
                "request_id": REQUEST_ID_CTX.get(),
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "client_ip": request.client.host if request.client else None,
            },
        )
        return response
