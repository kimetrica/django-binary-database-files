# Generated by Django 1.9.1 on 2016-10-11 18:11
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255, unique=True)),
                ("size", models.PositiveIntegerField(db_index=True)),
                ("content", models.BinaryField()),
                (
                    "created_datetime",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="Created datetime",
                    ),
                ),
                (
                    "_content_hash",
                    models.CharField(
                        blank=True,
                        db_column="content_hash",
                        db_index=True,
                        max_length=128,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "binary_database_files_file",
            },
        ),
    ]
