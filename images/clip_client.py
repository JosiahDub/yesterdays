"""
HTTP client for the embedding microservice (services/clip).

The service serves settings.EMBEDDING_MODEL_ID (PE-Core L/14@336). Every
response is checked against that model and settings.EMBEDDING_DIMENSION, so
a service running another model (e.g. mid-rollout) raises
ClipServiceMismatch instead of mixing two models' vectors in one column.

Callers should treat requests exceptions and ClipServiceMismatch (a
RuntimeError) like any other embedding failure; the search views already wrap
embedding calls accordingly.
"""

import requests
from django.conf import settings

_session = requests.Session()


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
    _require_url()
    response = _session.post(
        f"{settings.CLIP_SERVICE_URL}/embed/text",
        json={"text": text},
        timeout=settings.CLIP_SERVICE_TIMEOUT,
    )
    return _checked_embedding(response)


def get_image_embedding(image_bytes):
    """
    Encode image bytes into a unit-length embedding (list of floats).
    """
    _require_url()
    response = _session.post(
        f"{settings.CLIP_SERVICE_URL}/embed/image",
        data=image_bytes,
        headers={"Content-Type": "application/octet-stream"},
        timeout=settings.CLIP_SERVICE_TIMEOUT,
    )
    return _checked_embedding(response)
