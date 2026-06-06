"""
OpenTelemetry setup.

Exports traces as OTLP/JSON to stdout by default.
Set OTEL_EXPORTER_OTLP_ENDPOINT to ship to a collector (e.g. Grafana Cloud, Jaeger).

Auto-instrumented:
  - FastAPI (HTTP spans)
  - SQLAlchemy async (DB spans)
  - Requests / httpx (outbound HTTP spans, if used)
"""
import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def _build_resource() -> Resource:
    s = get_settings()
    return Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: s.APP_NAME,
            ResourceAttributes.SERVICE_VERSION: "1.0.0",
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: s.APP_ENV,
        }
    )


def setup_telemetry(app) -> None:  # noqa: ANN001
    """
    Call once inside the FastAPI lifespan *before* the app starts serving.
    Wires OTEL tracing into FastAPI and SQLAlchemy.
    """
    settings = get_settings()
    resource = _build_resource()
    provider = TracerProvider(resource=resource)

    # ── Exporter selection ────────────────────────────────────────────────────
    if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
        logger.info("otel_exporter=otlp endpoint=%s", settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    else:
        # Pretty JSON to stdout — picked up by DO log drain / any log aggregator
        exporter = ConsoleSpanExporter()
        logger.info("otel_exporter=console (stdout)")

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # ── Auto-instrument ───────────────────────────────────────────────────────
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=provider,
        excluded_urls="/health,/health/ready,/metrics",  # don't trace probes
    )
    SQLAlchemyInstrumentor().instrument(
        tracer_provider=provider,
        enable_commenter=True,
        commenter_options={},
    )

    logger.info("opentelemetry_initialized service=%s env=%s", settings.APP_NAME, settings.APP_ENV)
