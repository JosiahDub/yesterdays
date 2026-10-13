"""
HTTP client for the embedding microservice (services/clip).

The service serves settings.EMBEDDING_MODEL_ID (PE-Core L/14@336). Every
response is checked against that model and settings.EMBEDDING_DIMENSION, so
a service running another model (e.g. mid-rollout) raises
ClipServiceMismatch instead of mixing two models' vectors in one column.

Callers should treat requests exceptions and ClipServiceMismatch (a
RuntimeError) like any other embedding failure; the search views already wrap
embedding calls accordingly.

Every call is counted in clip_client_requests_total{operation, outcome} and
timed in clip_client_request_duration_seconds, so an unreachable service still
shows up in Prometheus. Only processes running the metrics server (the web
pods) are scraped; calls made inside Celery's prefork children are not.
"""

import time

import requests
from django.conf import settings
from prometheus_client import Counter, Histogram

_session = requests.Session()

REQUESTS = Counter(
    "clip_client_requests",
    "Calls to the embedding service, by operation and outcome.",
    ["operation", "outcome"],
)
REQUEST_DURATION = Histogram(
    "clip_client_request_duration_seconds",
    "Round-trip time of calls to the embedding service, failures included.",
    ["operation"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30),
)


class ClipServiceMismatch(RuntimeError):
    """The service answered with a different model or dimension than expected."""


def is_configured():
    return bool(settings.CLIP_SERVICE_URL)


def _require_url():
    if not settings.CLIP_SERVICE_URL:
        raise RuntimeError(
            "CLIP_SERVICE_URL is not configured; semantic search and embedding "
            "generation require the embedding service (services/clip)."
        )
    return settings.CLIP_SERVICE_URL


def _outcome(exc):
    # Timeout first: ConnectTimeout is both a Timeout and a ConnectionError.
    if isinstance(exc, requests.Timeout):
        return "timeout"
    if isinstance(exc, requests.ConnectionError):
        return "connection_error"
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return f"http_{exc.response.status_code}"
    if isinstance(exc, ClipServiceMismatch):
        return "mismatch"
    return "error"


def _embed(operation, **kwargs):
    url = _require_url()
    started = time.perf_counter()
    outcome = "ok"
    try:
        response = _session.post(
            f"{url}/embed/{operation}",
            timeout=settings.CLIP_SERVICE_TIMEOUT,
            **kwargs,
        )
        return _checked_embedding(response)
    except Exception as exc:
        outcome = _outcome(exc)
        raise
    finally:
        REQUEST_DURATION.labels(operation).observe(time.perf_counter() - started)
        REQUESTS.labels(operation, outcome).inc()


def _checked_embedding(response):
    response.raise_for_status()
    payload = response.json()
    model, dim = payload.get("model"), payload.get("dim")
    if (
        model != settings.EMBEDDING_MODEL_ID
        or dim != settings.EMBEDDING_DIMENSION
        or len(payload["embedding"]) != settings.EMBEDDING_DIMENSION
    ):
        raise ClipServiceMismatch(
            f"Embedding service returned model {model!r} ({dim}D); expected "
            f"{settings.EMBEDDING_MODEL_ID!r} ({settings.EMBEDDING_DIMENSION}D)"
        )
    return payload["embedding"]


def get_text_embedding(text):
    """
    Encode text into a unit-length embedding (list of floats).
    """
    return _embed("text", json={"text": text})


def get_image_embedding(image_bytes):
    """
    Encode image bytes into a unit-length embedding (list of floats).
    """
    return _embed(
        "image",
        data=image_bytes,
        headers={"Content-Type": "application/octet-stream"},
    )
