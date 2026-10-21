"""
Prometheus metrics, exposed at GET /metrics.

uvicorn runs a single process, so the default registry is enough; adding
--workers would need prometheus_client's multiprocess mode.
"""

from prometheus_client import Counter, Enum, Gauge, Histogram, Info

# Seconds; spans CPU text queries (~10ms) to cold or CPU-bound image work.
LATENCY_BUCKETS = (
    0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.25, 0.5, 0.75, 1, 2.5, 5, 10,
)

REQUESTS = Counter(
    "clip_requests",
    "Embedding requests by endpoint and response status.",
    ["endpoint", "status"],
)
REQUEST_DURATION = Histogram(
    "clip_request_duration_seconds",
    "Embedding request latency as seen by the service.",
    ["endpoint"],
    buckets=LATENCY_BUCKETS,
)

# Phases: decode/preprocess (vision) or tokenize (text), then lock_wait (queued
# behind the tower's single infer request) and infer.
PHASE_DURATION = Histogram(
    "clip_phase_duration_seconds",
    "Time spent in each phase of encoding, per tower.",
    ["tower", "phase"],
    buckets=LATENCY_BUCKETS,
)
INFLIGHT = Gauge(
    "clip_inflight_requests",
    "Requests being encoded by each tower, including those queued on its lock.",
    ["tower"],
)

IMAGE_BYTES = Histogram(
    "clip_image_bytes",
    "Size of request bodies sent to /embed/image.",
    buckets=[2**n for n in range(14, 26)],  # 16 KiB .. 32 MiB
)
TEXT_TOKENS = Histogram(
    "clip_text_tokens",
    "BPE tokens per text query, before truncation to the context length.",
    buckets=(2, 4, 8, 12, 16, 20, 24, 30, 40, 60, 100),
)
TEXT_TRUNCATED = Counter(
    "clip_text_truncated",
    "Text queries cut off at the model's context length.",
)

MODEL_STATE = Enum(
    "clip_model_state",
    "Whether the embedding model is loading, ready, or failed to load.",
    states=["loading", "ready", "failed"],
)
MODEL_LOAD_SECONDS = Gauge(
    "clip_model_load_seconds",
    "Time to compile and warm up the model (long when the kernel cache was cold).",
)
MODEL_INFO = Info(
    "clip_model",
    "The loaded model, with each tower's execution devices and precision.",
)


def set_model_info(model_id, devices):
    """Record /info's model and devices() result as clip_model_info labels."""
    labels = {"model": model_id}
    for tower, info in devices.items():
        labels[f"{tower}_devices"] = _label(info["devices"])
        labels[f"{tower}_precision"] = _label(info["precision"])
    MODEL_INFO.info(labels)


def _label(value):
    if isinstance(value, dict):
        return ",".join(f"{key}:{val}" for key, val in value.items())
    if isinstance(value, (list, tuple)):
        return ",".join(str(item) for item in value)
    return str(value)
