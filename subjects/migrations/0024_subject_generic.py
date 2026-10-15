"""Add ``Subject.generic``."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subjects", "0023_alter_subject_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="generic",
            field=models.BooleanField(
                default=False,
                help_text="If marked as generic, a subject will not be shown on the map.",
            ),
        ),
    ]
