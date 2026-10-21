"""
One-time export of Meta's PE-Core L/14@336 (via open_clip) to an OpenVINO IR
bundle.

Run from services/clip/ with the export dependency group:

    uv run --group export scripts/export_ir.py --parity PATH

Writes the IR models, BPE tokenizer files and metadata.json into model/
(which the dev compose stack bind-mounts directly), verifies the service's
own tokenizer, preprocessing and OpenVINO inference against open_clip, then
packs the bundle into a versioned tarball whose URL and sha256 feed the
release image build (see .github/workflows/clip-service.yml). Upload the
tarball to R2 and update the workflow variables when publishing a new bundle.

--parity points at the eval repo's parity fixture (data/export/parity-v1.json,
with the corpus JPEGs under ../images/): canonical open_clip tokens and
vectors for ~2000 texts and ~200 images. Without it, verification falls back
to a built-in sample of texts and synthetic images.
"""

import argparse
import base64
import gzip
import hashlib
import json
import sys
import tarfile
from pathlib import Path

import numpy as np
import open_clip
import openvino as ov
import timm
import torch
import transformers
from open_clip.tokenizer import default_bpe
from PIL import Image
from transformers import CLIPTokenizerFast

# The service's runtime code is what gets verified, so import it rather than
# re-implementing tokenization/preprocessing here.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.encoder import ClipEncoder, preprocess_image  # noqa: E402

MODEL_ID = "PE-Core-L-14-336"
PRETRAINED = "meta"
TARBALL_STEM = "pe-core-l14-336-ir"
# open_clip's PE-Core transform: squash to the square input with antialiased
# bilinear (PIL), then (x - 0.5) / 0.5. verify() checks the runtime matches it.
PREPROCESS = {
    "resize": "squash",
    "interpolation": "bilinear",
    "mean": [0.5, 0.5, 0.5],
    "std": [0.5, 0.5, 0.5],
}

SAMPLE_TEXTS = [
    "a photograph of a city street with a monument",
    "Monument Avenue, looking west from Lombardy St., ca. 1910",
    "Lee’s statue on “Monument Avenue”",
    "AT&amp;T building &amp;amp; parking lot",
    "No. 12½ East Main St., 3:45 p.m., 100%",
    "CafÃ© Rouge",
    "ﬁre station   with\ttabs\nand newlines",
    "東京 Tokyo 🚂",
    "a <|endoftext|> b <start_of_text> c",
    "the old tobacco warehouse on the canal " * 10,
    "!!!",
    "x",
]
STRATA_LIMIT = 8
TORCH_SAMPLES = 16

TEXT_COSINE_MIN = 0.999
IMAGE_COSINE_MIN = 0.999
PREPROCESS_MAX_ABS = 1e-5


class TextTower(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids):
        # Unnormalized: the service L2-normalizes after inference.
        return self.model.encode_text(input_ids)


class VisionTower(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, pixel_values):
        return self.model.encode_image(pixel_values)


def load():
    print(f"Loading {MODEL_ID} ({PRETRAINED}) …")
    model, _, transform = open_clip.create_model_and_transforms(
        MODEL_ID, pretrained=PRETRAINED
    )
    model.eval()
    return model, transform, open_clip.get_tokenizer(MODEL_ID)


def export(out_dir, bundle_version, model, oc_tokenizer):
    out_dir.mkdir(parents=True, exist_ok=True)
    context_length = oc_tokenizer.context_length
    image_size = model.visual.image_size
    image_size = max(image_size) if isinstance(image_size, (tuple, list)) else image_size

    print("Converting text tower …")
    example_ids = torch.zeros((1, context_length), dtype=torch.int64)
    text_ov = ov.convert_model(TextTower(model), example_input=example_ids)
    text_ov.reshape([-1, context_length])
    ov.save_model(text_ov, out_dir / "text.xml", compress_to_fp16=True)

    print("Converting vision tower …")
    example_pixels = torch.zeros((1, 3, image_size, image_size), dtype=torch.float32)
    vision_ov = ov.convert_model(VisionTower(model), example_input=example_pixels)
    vision_ov.reshape([-1, 3, image_size, image_size])
    ov.save_model(vision_ov, out_dir / "vision.xml", compress_to_fp16=True)

    tokenizer_files = save_tokenizer(out_dir, oc_tokenizer)

    with torch.no_grad():
        dim = model.encode_text(example_ids).shape[-1]
    metadata = {
        "model_id": MODEL_ID,
        "pretrained": PRETRAINED,
        "bundle_version": bundle_version,
        "dim": int(dim),
        "context_length": context_length,
        "image_size": int(image_size),
        "normalized": True,
        "preprocess": PREPROCESS,
        "tokenizer": {
            "sot": oc_tokenizer.sot_token_id,
            "eot": oc_tokenizer.eot_token_id,
            "pad": 0,
        },
        "exported_with": {
            "open_clip": open_clip.__version__,
            "timm": timm.__version__,
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "openvino": ov.__version__,
        },
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    names = ["metadata.json", "text.xml", "text.bin", "vision.xml", "vision.bin"]
    return names + sorted({Path(f).name for f in tokenizer_files})


def save_tokenizer(out_dir, oc_tokenizer):
    """
    PE-Core reuses OpenAI CLIP's BPE vocabulary; write it in HF's
    vocab.json/merges.txt form (open_clip's own rank order, HF's special-token
    names) so CLIPTokenizerFast can load it without torch.
    """
    special_names = {"<start_of_text>": "<|startoftext|>", "<end_of_text>": "<|endoftext|>"}
    vocab = {special_names.get(k, k): v for k, v in oc_tokenizer.encoder.items()}
    if sorted(vocab.values()) != list(range(len(vocab))):
        raise SystemExit("open_clip vocabulary is not a dense id range; aborting")
    # The slice SimpleTokenizer takes: skip the header, keep the merges its
    # vocabulary was built from.
    merges = gzip.open(default_bpe()).read().decode("utf-8").split("\n")
    merges = merges[1 : 49152 - 256 - 2 + 1]
    (out_dir / "vocab.json").write_text(json.dumps(vocab, ensure_ascii=False))
    (out_dir / "merges.txt").write_text("#version: 0.2\n" + "\n".join(merges) + "\n")

    hf = CLIPTokenizerFast(
        vocab_file=str(out_dir / "vocab.json"),
        merges_file=str(out_dir / "merges.txt"),
        model_max_length=oc_tokenizer.context_length,
    )
    files = hf.save_pretrained(out_dir)

    reloaded = CLIPTokenizerFast.from_pretrained(out_dir).get_vocab()
    if reloaded != vocab:
        raise SystemExit("Saved tokenizer vocabulary differs from open_clip's; aborting")
    # save_pretrained also lists files it skipped (e.g. an empty added_tokens.json).
    return [f for f in files if Path(f).exists()]


def load_parity(path):
    """Fixture texts/images, or built-in samples when no fixture is given."""
    if path is None:
        return [{"text": t} for t in SAMPLE_TEXTS], [], None
    fixture = json.loads(path.read_text())
    if fixture["model_id"] != MODEL_ID:
        raise SystemExit(f"Parity fixture is for {fixture['model_id']}, not {MODEL_ID}")
    return fixture["texts"], fixture["images"], path.parent.parent / "images"


def open_corpus_image(images_dir, image_id, size):
    # As the eval corpus vectors were computed: draft-decoded 1920px JPEG.
    img = Image.open(images_dir / f"{image_id // 1000:03d}" / f"{image_id}.jpg")
    img.draft("RGB", (size, size))
    return img.convert("RGB")


def decode_vector(encoded):
    return np.frombuffer(base64.b64decode(encoded), dtype="<f4")


def cosines(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    return (a * b).sum(-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1))


def report(label, values, minimum=None):
    values = np.asarray(values)
    line = (
        f"  {label}: n={len(values)} min={values.min():.6f} "
        f"median={np.median(values):.6f} mean={values.mean():.6f}"
    )
    print(line)
    if minimum is not None and values.min() < minimum:
        raise SystemExit(f"{label} below {minimum}; aborting")


def verify(out_dir, model, transform, oc_tokenizer, parity_path):
    """
    Check the service's runtime code (app/encoder.py) against open_clip:
    (a) token ids, exactly; (b) image preprocessing, to 1e-5; (c) OpenVINO
    CPU f32 vs torch fp32 vectors. Aborts on any failure.
    """
    texts, images, images_dir = load_parity(parity_path)
    encoder = ClipEncoder(out_dir, "CPU", "CPU", precision="f32")
    print(f"Runtime encoder devices: {encoder.devices()}")
    size = encoder.meta["image_size"]

    print(f"(a) Tokenizer parity on {len(texts)} texts …")
    live = oc_tokenizer([t["text"] for t in texts]).numpy()
    failures = 0
    for entry, expected in zip(texts, live):
        runtime = encoder.tokenize(entry["text"])[0]
        fixture = entry.get("tokens")
        if not np.array_equal(runtime, expected) or (
            fixture is not None and runtime.tolist() != fixture
        ):
            failures += 1
            if failures <= 10:
                print(f"  MISMATCH {entry['text'][:80]!r}")
                print(f"    runtime   {runtime.tolist()}")
                print(f"    open_clip {expected.tolist()}")
    if failures:
        raise SystemExit(f"{failures} tokenizer mismatches; aborting")
    print(f"  all {len(texts)} identical (fixture and live open_clip)")

    print("(b) Preprocessing parity …")
    if images:
        # One image per aspect-ratio/colour stratum, so tall, wide, square and
        # greyscale sources are all covered.
        by_stratum = {}
        for entry in images:
            by_stratum.setdefault(entry.get("stratum", entry["id"]), entry)
        samples = [
            open_corpus_image(images_dir, e["id"], size)
            for e in list(by_stratum.values())[:STRATA_LIMIT]
        ]
        torch_samples = [
            open_corpus_image(images_dir, e["id"], size)
            for e in images[:: max(1, len(images) // TORCH_SAMPLES)]
        ]
    else:
        rng = np.random.default_rng(0)
        samples = torch_samples = [
            Image.fromarray(rng.integers(0, 256, (h, w, 3), dtype=np.uint8))
            for w, h in ((1920, 1280), (900, 1800), (512, 512), (2400, 400))
        ]
    worst = 0.0
    for img in samples:
        runtime = preprocess_image(img, size, encoder.preprocess)
        reference = transform(img).numpy()[None]
        diff = float(np.abs(runtime - reference).max())
        worst = max(worst, diff)
        print(f"  {img.size[0]}x{img.size[1]}: max abs diff {diff:.2e}")
    if worst > PREPROCESS_MAX_ABS:
        raise SystemExit(f"Preprocessing differs by {worst}; aborting")

    print("(c) OpenVINO CPU f32 vs torch fp32 …")
    sample_texts = [t["text"] for t in texts[:: max(1, len(texts) // TORCH_SAMPLES)]]
    with torch.no_grad():
        torch_text = model.encode_text(oc_tokenizer(sample_texts)).numpy()
        torch_image = model.encode_image(
            torch.stack([transform(img) for img in torch_samples])
        ).numpy()
    report(
        "text cosine",
        cosines([encoder.encode_text(t) for t in sample_texts], torch_text),
        TEXT_COSINE_MIN,
    )
    report(
        "image cosine",
        cosines([encoder.encode_pil(img) for img in torch_samples], torch_image),
        IMAGE_COSINE_MIN,
    )

    if parity_path is None:
        return
    print("Fixture vectors (open_clip fp32 on CUDA) vs OpenVINO CPU f32, informational …")
    report(
        "text cosine",
        cosines(
            [encoder.encode_text(t["text"]) for t in texts],
            [decode_vector(t["vector"]) for t in texts],
        ),
    )
    image_vectors = []
    for entry in images:
        path = images_dir / f"{entry['id'] // 1000:03d}" / f"{entry['id']}.jpg"
        image_vectors.append(encoder.encode_image(path.read_bytes()))
    report(
        "image cosine (JPEG bytes through encode_image)",
        cosines(image_vectors, [decode_vector(e["vector"]) for e in images]),
    )


def pack(out_dir, bundle_version, names):
    tar_path = out_dir.parent / f"{TARBALL_STEM}-{bundle_version}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        for name in names:
            tar.add(out_dir / name, arcname=name)
    digest = hashlib.sha256(tar_path.read_bytes()).hexdigest()
    print(f"\nBundle: {tar_path}")
    print(f"Size:   {tar_path.stat().st_size / 1e6:.0f} MB")
    print(f"SHA256: {digest}")
    print(
        "\nUpload to R2, then set MODEL_BUNDLE_URL and MODEL_BUNDLE_SHA256 "
        "in .github/workflows/clip-service.yml"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).parent.parent / "model"
    )
    parser.add_argument("--bundle-version", default="v1")
    parser.add_argument(
        "--skip-pack", action="store_true", help="Only populate --out (for local dev)"
    )
    parser.add_argument(
        "--parity", type=Path, help="Eval repo parity fixture (parity-v1.json)"
    )
    args = parser.parse_args()

    model, transform, oc_tokenizer = load()
    names = export(args.out, args.bundle_version, model, oc_tokenizer)
    verify(args.out, model, transform, oc_tokenizer, args.parity)
    if not args.skip_pack:
        pack(args.out, args.bundle_version, names)


if __name__ == "__main__":
    main()
