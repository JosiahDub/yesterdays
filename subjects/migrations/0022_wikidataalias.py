"""Add ``WikidataAlias``, mirrored from each closure load.

No data step: existing items are filled from the Memgraph mirror by the
``rebuild_wikidata_aliases`` management command, since migrations don't talk
to Memgraph.
"""

import django.db.models.deletion
from django.contrib.postgres.indexes import GinIndex
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subjects", "0021_osmelement_osm_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="WikidataAlias",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        help_text="Language key as mirrored in Memgraph (e.g. en, mul, en_gb)",
                        max_length=35,
                    ),
                ),
                ("alias", models.CharField(max_length=500)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="aliases",
                        to="subjects.wikidataitem",
                    ),
                ),
            ],
            options={
                "ordering": ["language", "alias"],
                "indexes": [
                    GinIndex(
                        fields=["alias"],
                        name="wikidataalias_alias_trgm",
                        opclasses=["gin_trgm_ops"],
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("item", "language", "alias"),
                        name="wikidataalias_unique",
                    )
                ],
            },
        ),
    ]
