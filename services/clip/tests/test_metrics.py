import threading

import numpy as np
import pytest
from fastapi.testclient import TestClient
from prometheus_client import REGISTRY

from app.encoder import CLIP_TOKENIZER, ClipEncoder
from app.main import app
from app.metrics import MODEL_INFO, set_model_info


def sample(name, **labels):
    return REGISTRY.get_sample_value(name, labels) or 0.0


class StubTokenizer:
    """One token id per word, like a vocabulary of whole words."""

    def __call__(self, words, add_special_tokens):
        return {"input_ids": [[100] for _ in words]}


class StubRequest:
    def infer(self, inputs):
        return {"output": np.array([[3.0, 4.0]])}


def stub_encoder():
    # Skips __init__, which compiles the OpenVINO models.
    encoder = ClipEncoder.__new__(ClipEncoder)
    encoder.meta = {"context_length": 32}
    encoder.special = CLIP_TOKENIZER
    encoder._tokenizer = StubTokenizer()
    return encoder


# Encoder


def test_long_text_is_counted_as_truncated():
    encoder = stub_encoder()
    before = sample("clip_text_truncated_total")
    encoder.tokenize("word " * 30)  # fills the 30 slots between sot and eot
    assert sample("clip_text_truncated_total") == before
    encoder.tokenize("word " * 31)
    assert sample("clip_text_truncated_total") == before + 1


def test_infer_records_lock_wait_and_infer():
    encoder = stub_encoder()
    labels = {"tower": "text"}
    before = {
        phase: sample("clip_phase_duration_seconds_count", phase=phase, **labels)
        for phase in ("lock_wait", "infer")
    }
    vector = encoder._infer("text", threading.Lock(), StubRequest(), None)
    assert vector == pytest.approx([0.6, 0.8])
    for phase, count in before.items():
        assert (
            sample("clip_phase_duration_seconds_count", phase=phase, **labels)
            == count + 1
        )


def test_model_info_flattens_devices():
    set_model_info(
        "PE-Core-L-14-336",
        {
            "text": {"devices": ["CPU"], "precision": "f32"},
            "vision": {"devices": "unknown", "precision": {"GPU": "f16", "CPU": "f32"}},
        },
    )
    assert MODEL_INFO._value == {
        "model": "PE-Core-L-14-336",
        "text_devices": "CPU",
        "text_precision": "f32",
        "vision_devices": "unknown",
        "vision_precision": "GPU:f16,CPU:f32",
    }


# HTTP (no lifespan, so the model never loads)


def test_embed_requests_are_counted_by_status():
    client = TestClient(app)
    labels = {"endpoint": "/embed/text", "status": "503"}
    before = sample("clip_requests_total", **labels)
    assert client.post("/embed/text", json={"text": "a street"}).status_code == 503
    assert sample("clip_requests_total", **labels) == before + 1
    assert sample("clip_request_duration_seconds_count", endpoint="/embed/text") >= 1


def test_probes_are_not_measured():
    client = TestClient(app)
    client.get("/healthz")
    assert sample("clip_requests_total", endpoint="/healthz", status="200") == 0


def test_metrics_endpoint_serves_exposition_format():
    response = TestClient(app).get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert 'clip_model_state{clip_model_state="loading"} 1.0' in response.text
