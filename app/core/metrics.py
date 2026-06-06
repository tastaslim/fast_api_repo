"""
Prometheus metrics.

Exposes /metrics (Prometheus text format) via prometheus-fastapi-instrumentator.
Adds custom business metrics on top of the default HTTP instrumentation.

Scraped by:
  - DO App Platform built-in Prometheus (if enabled)
  - Any sidecar / external Prometheus via HTTP scrape
"""
from prometheus_client import Counter, Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# ── Custom business metrics ────────────────────────────────────────────────────

PRODUCT_CREATED = Counter(
    "product_created_total",
    "Total number of products created",
)

PRODUCT_DELETED = Counter(
    "product_deleted_total",
    "Total number of products deleted",
)

PRODUCT_STOCK_GAUGE = Gauge(
    "product_stock_units",
    "Current stock level per SKU",
    labelnames=["sku"],
)

DB_QUERY_DURATION = Histogram(
    "db_query_duration_seconds",
    "Duration of DB operations",
    labelnames=["operation"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)


def setup_metrics(app) -> None:  # noqa: ANN001
    """
    Attaches prometheus-fastapi-instrumentator to the app.
    Exposes /metrics — exclude from auth via router ordering (health prefix, no JWT dep).
    """
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=False,
        excluded_handlers=["/health", "/health/ready", "/metrics"],
        body_handlers=[],
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
