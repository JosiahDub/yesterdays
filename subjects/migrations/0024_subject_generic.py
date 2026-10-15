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
                help_text="Whether this subject is a generic concept rather than a specific entity",
            ),
        ),
    ]
