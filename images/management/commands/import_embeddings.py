"""
Load precomputed image embeddings from an .npz file into Image.embedding.

The file (from ``export_embeddings`` or the evaluation repo's export_seed.py)
holds ``ids``, ``vectors``, a JSON ``meta`` string and, optionally, ``urls``:
the displayed permalink each vector was computed from. It is rejected unless
meta's model id and the vectors' dimension match settings.EMBEDDING_MODEL_ID
and settings.EMBEDDING_DIMENSION and every vector is unit length, so vectors
from two models can't end up side by side in the column.

Only images whose embedding is still NULL are written, so re-running an
import never overwrites vectors generate_embeddings has since replaced. With
``urls``, an image is also only written while its displayed permalink still
matches: that catches a database whose ids belong to other images (a dev or
staging copy that diverged from production) and images re-transformed since
the vectors were computed. Ids with no matching image are counted and skipped.

Usage:
    python manage.py import_embeddings <path-or-url> [--refresh-stats]
        [--model-id ID --dimension N]
"""

import json
import tempfile
from pathlib import Path

import numpy as np
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from images.models import Image
from images.tasks import refresh_collection_embedding_stats

# Rows per transaction. Vectors stay in the file's dtype (float16 for seeds)
# and are expanded one batch at a time: the import pod has a 500Mi limit, and
# a whole seed in float32 plus its temporaries doesn't fit beside Django.
BATCH_SIZE = 500
# Seed files store float16 vectors, whose norms drift by ~1e-3.
NORM_TOLERANCE = 1e-2


class Command(BaseCommand):
    help = "Import image embeddings from an .npz file into rows lacking one"

    def add_arguments(self, parser):
        parser.add_argument("source", help="Path or http(s) URL of the .npz file")
        parser.add_argument(
            "--refresh-stats",
            action="store_true",
            help="Recompute every collection's mean embedding afterwards",
        )
        # Overrides for restoring a backup from another model during a
        # rollback; normally the settings are the only acceptable values.
        parser.add_argument(
            "--model-id",
            help="Required meta model id (default: settings.EMBEDDING_MODEL_ID)",
        )
        parser.add_argument(
            "--dimension",
            type=int,
            help="Required vector dimension (default: settings.EMBEDDING_DIMENSION)",
        )

    def handle(self, *args, **options):
        model_id = options["model_id"] or settings.EMBEDDING_MODEL_ID
        dimension = options["dimension"] or settings.EMBEDDING_DIMENSION

        with tempfile.TemporaryDirectory() as tmp:
            path = self._fetch(options["source"], Path(tmp))
            try:
                with np.load(path, allow_pickle=False) as data:
                    ids = data["ids"].astype(np.int64)
                    vectors = data["vectors"]
                    meta = json.loads(str(data["meta"]))
                    urls = data["urls"] if "urls" in data else None
            except (OSError, KeyError, ValueError) as e:
                raise CommandError(f"Not a readable embeddings file: {e}") from e

        self.stdout.write(f"File meta: {json.dumps(meta)}")
        if meta.get("model_id") != model_id:
            raise CommandError(
                f"File holds {meta.get('model_id')!r} embeddings; expected {model_id!r}"
            )
        if vectors.ndim != 2 or vectors.shape[1] != dimension:
            raise CommandError(
                f"File vectors have shape {vectors.shape}; expected {dimension} columns"
            )
        if not len(ids) or len(ids) != len(vectors):
            raise CommandError(f"{len(ids)} ids but {len(vectors)} vectors")
        if urls is None:
            self.stdout.write(
                self.style.WARNING(
                    "File has no urls: ids are trusted to name the same images "
                    "as where the vectors were computed"
                )
            )
        elif len(urls) != len(ids):
            raise CommandError(f"{len(ids)} ids but {len(urls)} urls")
        # Checked for the whole file before anything is written.
        norms = np.concatenate(
            [
                np.linalg.norm(_floats(vectors[start : start + BATCH_SIZE]), axis=1)
                for start in range(0, len(vectors), BATCH_SIZE)
            ]
        )
        if not np.all(np.abs(norms - 1) <= NORM_TOLERANCE):
            raise CommandError(
                f"Vectors are not unit length (norms {norms.min():.4f}–{norms.max():.4f})"
            )

        totals = dict.fromkeys(("written", "embedded", "mismatched", "unknown"), 0)
        for start in range(0, len(ids), BATCH_SIZE):
            batch = slice(start, start + BATCH_SIZE)
            # Dividing by the norm undoes float16 rounding, so stored
            # vectors are exactly unit length.
            counts = self._write_batch(
                ids[batch].tolist(),
                (_floats(vectors[batch]) / norms[batch, None]).tolist(),
                urls[batch].tolist() if urls is not None else None,
            )
            for key, count in counts.items():
                totals[key] += count
            self.stdout.write(
                f"{min(start + BATCH_SIZE, len(ids))}/{len(ids)}: "
                + ", ".join(f"{count} {key}" for key, count in totals.items())
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {totals['written']} embeddings; skipped "
                f"{totals['embedded']} images that already had one, "
                f"{totals['mismatched']} whose displayed image differs from the "
                f"file's and {totals['unknown']} ids with no image"
            )
        )

        if options["refresh_stats"]:
            self.stdout.write("Refreshing collection embedding stats…")
            refresh_collection_embedding_stats()
            self.stdout.write(
                self.style.SUCCESS("Collection embedding stats refreshed")
            )

    def _fetch(self, source, tmp_dir):
        """A local path to the file, downloading it first if source is a URL."""
        if not source.startswith(("http://", "https://")):
            return source
        path = tmp_dir / "embeddings.npz"
        self.stdout.write(f"Downloading {source}…")
        try:
            with requests.get(source, stream=True, timeout=60) as response:
                response.raise_for_status()
                with path.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=1 << 20):
                        f.write(chunk)
        except requests.RequestException as e:
            raise CommandError(f"Download failed: {e}") from e
        return path

    def _write_batch(self, ids, vectors, urls):
        """Fill NULL embeddings for one batch; returns counts by outcome."""
        expected_url = dict(zip(ids, urls)) if urls is not None else {}
        with transaction.atomic():
            current = {
                image_id: (embedding is not None, transformed or permalink)
                for image_id, embedding, transformed, permalink in Image.objects.filter(
                    id__in=ids
                )
                .select_for_update()
                .values_list("id", "embedding", "transformed_permalink", "permalink")
            }
            counts = {"written": 0, "embedded": 0, "mismatched": 0, "unknown": 0}
            rows = []
            for image_id, vector in zip(ids, vectors):
                if image_id not in current:
                    counts["unknown"] += 1
                elif current[image_id][0]:
                    counts["embedded"] += 1
                elif (
                    urls is not None and expected_url[image_id] != current[image_id][1]
                ):
                    counts["mismatched"] += 1
                else:
                    rows += [image_id, vector]
            if rows:
                values = ", ".join(
                    ["(%s::integer, %s::double precision[])"] * (len(rows) // 2)
                )
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                        UPDATE images_image AS i
                        SET embedding = v.embedding
                        FROM (VALUES {values}) AS v(id, embedding)
                        WHERE i.id = v.id AND i.embedding IS NULL
                        """,
                        rows,
                    )
                    counts["written"] = cursor.rowcount
        return counts


def _floats(rows):
    return rows.astype(np.float32)
