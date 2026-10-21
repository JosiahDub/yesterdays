"""
Switch Image.embedding from CLIP ViT-L/14@336 (768D) to PE-Core L/14@336
(1024D).

The column is replaced rather than converted: the old vectors are useless to
the new model, and a fresh column frees them at once. Everything derived from
them goes too (collection means, nightly duplicate candidates); dismissed
duplicate pairs stay, since they are human decisions. The HNSW indexes are
rebuilt on the empty column, so filling it (manage.py import_embeddings, then
generate_embeddings --force) inserts into a live index.

Embedding features return nothing between this migration and the import; see
docs/dev/deployment/clip-service.md for the cutover runbook. Reversing it
restores the 768D indexes on an empty column; reload the old vectors from the
export_embeddings backup.

The dimensions are frozen here on purpose (not read from settings), like any
migration's schema.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import connection, migrations, models

INDEXES = (
    ("images_image_embedding_hnsw_idx", ""),
    (
        "images_image_searchable_embedding_hnsw_idx",
        "WHERE is_searchable = true AND embedding IS NOT NULL",
    ),
)


def _create_indexes(schema_editor, dimension):
    if connection.vendor != "postgresql":
        return
    for name, predicate in INDEXES:
        schema_editor.execute(f"""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS {name}
            ON images_image USING hnsw ((embedding::vector({dimension})) vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
            {predicate};
        """)


def _drop_indexes(schema_editor):
    if connection.vendor != "postgresql":
        return
    for name, _ in INDEXES:
        schema_editor.execute(f"DROP INDEX CONCURRENTLY IF EXISTS {name};")


def drop_indexes(apps, schema_editor):
    _drop_indexes(schema_editor)


def create_clip_indexes(apps, schema_editor):
    _create_indexes(schema_editor, 768)


def create_pe_core_indexes(apps, schema_editor):
    _create_indexes(schema_editor, 1024)


class Migration(migrations.Migration):
    # atomic = False is required for CREATE/DROP INDEX CONCURRENTLY
    atomic = False

    dependencies = [
        ("images", "0068_sitesettings_home_subjects_order"),
    ]

    operations = [
        migrations.RunPython(drop_indexes, create_clip_indexes),
        migrations.RemoveField(model_name="image", name="embedding"),
        migrations.AddField(
            model_name="image",
            name="embedding",
            field=ArrayField(
                base_field=models.FloatField(),
                blank=True,
                null=True,
                size=None,
                help_text="PE-Core L/14@336 embedding of the displayed image (settings.EMBEDDING_MODEL_ID, unit length)",
            ),
        ),
        migrations.RunSQL(
            "DELETE FROM images_collectionembeddingstats;"
            " DELETE FROM images_duplicateimagepair;",
            migrations.RunSQL.noop,
        ),
        migrations.RunPython(create_pe_core_indexes, drop_indexes),
    ]
