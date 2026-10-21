"""
Export every stored image embedding to an .npz file.

The file holds ``ids`` (int64), ``vectors`` (one row per id), ``urls`` (each
image's displayed permalink at export time, which import_embeddings checks
before writing) and ``meta`` (a JSON string: model id, dimension, count,
dtype, export time), the format ``import_embeddings`` reads. Used to back up
the vectors before a model switch and to compare regenerated vectors against
an import.

Only Django and numpy are needed, so the module also runs piped through
``manage.py shell`` on an image that predates it; see
docs/dev/deployment/clip-service.md.

Usage:
    python manage.py export_embeddings /tmp/embeddings.npz
        [--model-id ID] [--dtype float32|float16] [--limit N]
"""

import json

import numpy as np
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from images.models import Image


class Command(BaseCommand):
    help = "Export image embeddings to an .npz file (ids, vectors, meta)"

    def add_arguments(self, parser):
        parser.add_argument("path", help="Output .npz file")
        parser.add_argument(
            "--model-id",
            help="Model the stored vectors came from, recorded in meta "
            "(default: settings.EMBEDDING_MODEL_ID)",
        )
        parser.add_argument(
            "--dtype",
            choices=["float32", "float16"],
            default="float32",
            help="Vector precision in the file (default: float32)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Only export the first N embedded images by id (for spot checks)",
        )

    def handle(self, *args, **options):
        model_id = options["model_id"] or settings.EMBEDDING_MODEL_ID
        rows = (
            Image.objects.filter(embedding__isnull=False)
            .order_by("id")
            .values_list("id", "embedding", "transformed_permalink", "permalink")
        )
        if options["limit"]:
            rows = rows[: options["limit"]]

        # Filled in place, in the output dtype: the import pod this runs in
        # has a 500Mi limit, too little for a list of vectors plus a stacked
        # copy.
        count = rows.count()
        if not count:
            raise CommandError("No images have embeddings; nothing to export.")
        ids = np.empty(count, dtype=np.int64)
        matrix, urls = None, []
        for n, (image_id, embedding, transformed, permalink) in enumerate(
            rows.iterator(chunk_size=2000)
        ):
            if n == count:  # embedded since the count; leave them out
                break
            if matrix is None:
                matrix = np.empty((count, len(embedding)), dtype=options["dtype"])
            elif len(embedding) != matrix.shape[1]:
                raise CommandError(
                    f"Stored embeddings mix dimensions {matrix.shape[1]} and "
                    f"{len(embedding)} (image {image_id})"
                )
            ids[n] = image_id
            matrix[n] = embedding
            urls.append(transformed or permalink)
        ids, matrix = ids[: len(urls)], matrix[: len(urls)]

        meta = {
            "model_id": model_id,
            "dim": matrix.shape[1],
            "count": len(ids),
            "dtype": options["dtype"],
            "source": "manage.py export_embeddings",
            "exported_at": timezone.now().isoformat(),
        }
        np.savez(
            options["path"],
            ids=ids,
            vectors=matrix,
            urls=np.array(urls),
            meta=np.array(json.dumps(meta)),
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(ids)} {matrix.shape[1]}D embeddings ({model_id}) "
                f"to {options['path']}"
            )
        )
