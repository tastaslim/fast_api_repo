from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import auth, health, products
from app.core.config import get_settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging
from app.core.metrics import setup_metrics
from app.core.middleware import CorrelationIDMiddleware, RequestLoggingMiddleware
from app.core.telemetry import setup_telemetry

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    setup_telemetry(app)   # OTEL auto-instrumentation (FastAPI + SQLAlchemy)
    yield
    # teardown: flush OTEL BatchSpanProcessor, close background workers


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        # Disable interactive docs in production — no surface for enumeration
        docs_url="/docs" if settings.APP_ENV != "production" else None,
        redoc_url="/redoc" if settings.APP_ENV != "production" else None,
        openapi_url="/openapi.json" if settings.APP_ENV != "production" else None,
        lifespan=lifespan,
    )

    # ── Middleware (outermost → innermost, Starlette wraps in reverse order) ──
    # 1. CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # tighten per-environment via env var
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 2. Correlation ID — generates / propagates X-Request-ID
    app.add_middleware(CorrelationIDMiddleware)
    # 3. Structured access logging
    app.add_middleware(RequestLoggingMiddleware)
    # 4. Rate limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # ── Exception handlers ────────────────────────────────────────────────────
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # ── Prometheus /metrics ───────────────────────────────────────────────────
    setup_metrics(app)

    # ── Routers ───────────────────────────────────────────────────────────────
    prefix = settings.API_V1_PREFIX
    app.include_router(health.router)          # /health, /health/ready — no auth
    app.include_router(auth.router, prefix=prefix)
    app.include_router(products.router, prefix=prefix)

    return app


app = create_app()
