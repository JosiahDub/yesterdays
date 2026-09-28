"""
Django management command to generate CLIP embeddings for images.

Embeddings are produced by the CLIP microservice (services/clip), reached via
``CLIP_SERVICE_URL``. This command downloads each image, shrinks it, and posts
it to the service; the service handles preprocessing and encoding.

With ``--queue`` the work is handed to the background Celery queue instead of
running in this process.

Usage:
    python manage.py generate_embeddings [--batch-size 100] [--concurrency 8]
                                         [--force] [--image-ids 1,2,3] [--queue]
"""

from concurrent.futures import ThreadPoolExecutor
from itertools import islice

from django.core.management.base import BaseCommand, CommandError

from images import clip_client
from images.models import Image
from images.tasks import embed_image_url, generate_embeddings_batch


class Command(BaseCommand):
    help = "Generate CLIP embeddings for images via the CLIP service"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of images to commit to the database per batch (default: 100)",
        )
        # The CLIP service encodes vision requests serially (one infer request
        # behind a lock, per replica), so raising concurrency past the replica
        # count only stacks requests behind that lock until they hit
        # CLIP_SERVICE_TIMEOUT.
        parser.add_argument(
            "--concurrency",
            type=int,
            default=2,
            help="Number of images to encode in parallel (default: 2)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate embeddings for images that already have them",
        )
        parser.add_argument(
            "--image-ids",
            type=str,
            help="Comma-separated list of specific image IDs to process",
        )
        parser.add_argument(
            "--queue",
            action="store_true",
            help="Queue a background Celery task instead of running here",
        )

    def handle(self, *args, **options):
        if not clip_client.is_configured():
            raise CommandError(
                "CLIP_SERVICE_URL is not set. This command requires the CLIP "
                "embedding service (services/clip) to be running and configured."
            )

        images_queryset = self.get_images_queryset(options)
        total_images = images_queryset.count()

        if total_images == 0:
            self.stdout.write(self.style.WARNING("No images found to process."))
            return

        if options["queue"]:
            # options["image_ids"] is a list[int] (or None) by now:
            # get_images_queryset() parsed the --image-ids string in place.
            # The task receives it as-is, so it must stay JSON-serializable.
            # --batch-size and --concurrency don't apply here; the task
            # uses its own EMBEDDING_TASK_BATCH_SIZE and runs serially.
            generate_embeddings_batch.delay(
                force=options["force"], image_ids=options["image_ids"]
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Queued embedding generation for {total_images} images"
                )
            )
            return

        batch_size = options["batch_size"]
        concurrency = options["concurrency"]
        self.stdout.write(
            self.style.SUCCESS(
                f"Processing {total_images} images "
                f"(commit batch {batch_size}, concurrency {concurrency})"
            )
        )

        processed_count = 0
        failed_count = 0
        batch_num = 0

        iterator = images_queryset.iterator(chunk_size=batch_size)
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            while batch_images := list(islice(iterator, batch_size)):
                batch_num += 1
                self.stdout.write(f"Processing batch {batch_num}...")

                batch_processed, batch_failed = self.process_batch(batch_images, pool)
                processed_count += batch_processed
                failed_count += batch_failed

                self.stdout.write(
                    f"Batch complete: {batch_processed} processed, {batch_failed} failed"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Embedding generation complete: {processed_count} processed, "
                f"{failed_count} failed"
            )
        )

    def get_images_queryset(self, options):
        """Get the queryset of images to process"""
        queryset = Image.objects.only("id", "permalink", "embedding")

        if options["image_ids"]:
            # Overwrite the raw "1,2,3" string with the parsed list[int] so
            # that handle() can pass it straight to generate_embeddings_batch
            # for --queue. Don't re-parse options["image_ids"] after this.
            try:
                options["image_ids"] = [
                    int(id.strip()) for id in options["image_ids"].split(",")
                ]
            except ValueError:
                raise CommandError(
                    "Invalid image IDs format. Use comma-separated integers."
                )
            queryset = queryset.filter(id__in=options["image_ids"])

        # Filter out images that already have embeddings unless --force is used
        if not options["force"]:
            queryset = queryset.filter(embedding__isnull=True)

        return queryset.order_by("id")

    def process_batch(self, batch_images, pool) -> tuple[int, int]:
        """Encode a batch of images concurrently and bulk-save the results."""
        successful_images = list(pool.map(self.embed_image, batch_images))
        successful_images = [image for image in successful_images if image is not None]

        if successful_images:
            Image.objects.bulk_update(successful_images, ["embedding"])

        return len(successful_images), len(batch_images) - len(successful_images)

    def embed_image(self, image):
        """Set an image's embedding from the service.

        Returns the mutated Image on success (for bulk_update), or None on
        failure (already logged).
        """
        try:
            image.embedding = embed_image_url(image.permalink)
            return image
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error processing image {image.id}: {e}")
            )
            return None
