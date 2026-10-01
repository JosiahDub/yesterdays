"""Drop the unique constraint on ``Subject.slug``.

Subject URLs are keyed by Q-ID now, so the slug is cosmetic and two
subjects sharing a label no longer collide.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subjects", "0022_wikidataalias"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="slug",
            field=models.SlugField(),
        ),
    ]
